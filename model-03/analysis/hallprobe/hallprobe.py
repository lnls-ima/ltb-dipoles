#!/usr/bin/env python-sirius

"""."""

import os as _os
import sys as _sys
from siriuspy import util as _util
import templates as _templates
import pickle as _pic
import numpy as _np


# text templates
_rawfield = _templates.rawfield
_trajectory = _templates.trajectory
_multipoles = _templates.multipoles
_model = _templates.model
_help = _templates.help


class FMapAnalysis:
    """."""

    def __init__(self,
                 magnet,
                 curlabel,
                 path_analysis,
                 path_fmap,
                 beam_energy,
                 rx_init,
                 s_step):
        """."""
        self.magnet = magnet
        self.curlabel = curlabel
        self.path_analysis = path_analysis
        self.path_fmap = path_fmap
        self.beam_energy = beam_energy
        self.rx_init = rx_init
        self.s_step = s_step
        if not _os.path.exists(path_analysis):
            _os.makedirs(path_analysis)

    def files_create(self):
        """."""
        self._create_rawfield_in()
        self._create_trajectory_in()
        self._create_multipoles_in()
        self._create_model_in()

    def files_read_results_rawfield(self):
        """."""
        fname = self.path_analysis + '/rawfield.out'
        with open(fname, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if 'main_coil_current' in line:
                self.results_current = float(line.split()[1])

    def files_read_results_trajectory(self):
        """."""
        fname = self.path_analysis + '/trajectory.out'
        with open(fname, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if 'horizontal_deflection_angle' in line:
                self.results_angle = float(line.split()[1])
            elif 'rx position of reference' in line:
                self.results_rx_ref = float(line.split()[5])
            # elif 'initial rx position' in line:
            #     self.results_rx_init = float(line.split()[5])

    def files_read_results_multipoles(self):
        """."""
        fname = self.path_analysis + '/multipoles.out'
        with open(fname, 'r') as f:
            lines = f.readlines()

        self.multipoles_normal = {}
        for line in lines:
            if 'r0_for_relative_multipoles' in line:
                self.reference_r0 = float(line.split()[1])/1000.0
            for n in range(30):
                nstr = 'n={:02d}'.format(n)
                if nstr in line:
                    dstr = line.split()
                    self.multipoles_normal[n] = float(dstr[2])

    def cmd_clean(self):
        """."""
        path = self.path_analysis
        cmd = 'cd ' + path + '; fac-fma-analysis.py clean'
        _os.system(cmd)

    def cmd_rawfield(self):
        """."""
        path = self.path_analysis
        cmd = 'cd ' + path + '; fac-fma-analysis.py rawfield'
        _os.system(cmd)

    def cmd_trajectory(self):
        """."""
        path = self.path_analysis
        cmd = 'cd ' + path + '; fac-fma-analysis.py trajectory'
        _os.system(cmd)

    def cmd_multipoles(self):
        """."""
        path = self.path_analysis
        cmd = 'cd ' + path + '; fac-fma-analysis.py multipoles'
        _os.system(cmd)

    def cmd_model(self):
        """."""
        path = self.path_analysis
        cmd = 'cd ' + path + '; fac-fma-analysis.py model'
        _os.system(cmd)

    def cmd_run(self):
        """."""
        path = self.path_analysis
        cmd = 'cd ' + path + '; fac-fma-analysis.py run'
        _os.system(cmd)

    def analysis_trajectory(self):
        """."""
        self.cmd_clean()
        self.files_create()
        self.cmd_rawfield()
        self.cmd_trajectory()
        self.files_read_results_rawfield()
        self.files_read_results_trajectory()

    # --- auxilliary method ---

    def _create_rawfield_in(self):
        text = self._process_text(_rawfield)
        fname = self.path_analysis + '/rawfield.in'
        with open(fname, 'w') as f:
            f.write(text)

    def _create_trajectory_in(self):
        text = self._process_text(_trajectory)
        fname = self.path_analysis + '/trajectory.in'
        with open(fname, 'w') as f:
            f.write(text)

    def _create_multipoles_in(self):
        text = self._process_text(_multipoles)
        fname = self.path_analysis + '/multipoles.in'
        with open(fname, 'w') as f:
            f.write(text)

    def _create_model_in(self):
        text = self._process_text(_model)
        fname = self.path_analysis + '/model.in'
        with open(fname, 'w') as f:
            f.write(text)

    def _process_text(self, text):
        t = text
        t = t.replace('TIMESTAMP', _util.get_timestamp())
        t = t.replace('MAGNET', self.magnet)
        t = t.replace('CONFIG_NAME', self.magnet+'-'+self.curlabel)
        t = t.replace('FIELDMAP_FNAME', self.path_fmap)
        t = t.replace('BEAM_ENERGY', str(self.beam_energy))
        t = t.replace('RX_INIT', str(self.rx_init))
        t = t.replace('S_STEP', str(self.s_step))
        return t


class FMapAnalysisProduction:
    """."""

    _path_analysis = (
        '/home/fac_files/lnls-ima/tb-dipoles/model-03'
        '/analysis/hallprobe/')

    _path_measurements = (
        '/home/fac_files/lnls-ima/tb-dipoles/model-03'
        '/measurement/magnetic/hallprobe/')

    def __init__(self,
                 magnet,
                 curlabel,
                 fmap_fname,
                 beam_energy,
                 rx_init,
                 s_step):
        """."""
        self.magnet = magnet
        self.curlabel = curlabel
        self.beam_energy = beam_energy
        self.path_analysis = FMapAnalysisProduction._path_analysis + \
            self.magnet + '/' + self.curlabel + '/'
        self.path_measurement = FMapAnalysisProduction._path_measurements + \
            self.magnet + '/'
        self.path_fmap = self.path_measurement + fmap_fname
        self.s_step = abs(s_step)
        self.analysis_neg = FMapAnalysis(self.magnet,
                                         self.curlabel,
                                         self.path_analysis + 'z-negative',
                                         self.path_fmap,
                                         self.beam_energy,
                                         rx_init,
                                         -1.0*self.s_step)
        self.analysis_pos = FMapAnalysis(self.magnet,
                                         self.curlabel,
                                         self.path_analysis + 'z-positive',
                                         self.path_fmap,
                                         self.beam_energy,
                                         rx_init,
                                         +1.0*self.s_step)

    def files_create(self):
        """."""
        self.analysis_pos.files_create()
        self.analysis_neg.files_create()

    def files_clean(self):
        """."""
        self.analysis_pos.files_clean()
        self.analysis_neg.files_clean()

    def files_read_results(self):
        """."""
        self.analysis_pos.files_read_results_rawfield()
        self.analysis_neg.files_read_results_rawfield()
        self.analysis_pos.files_read_results_trajectory()
        self.analysis_neg.files_read_results_trajectory()
        self.results_angle = self.analysis_pos.results_angle - \
            self.analysis_neg.results_angle
        self.analysis_pos.files_read_results_multipoles()
        self.analysis_neg.files_read_results_multipoles()
        self.multipoles_normal = {}
        self.multipoles_normal_relative = {}
        r0 = self.analysis_pos.reference_r0
        mm = (self.analysis_pos.multipoles_normal[0] +
              self.analysis_neg.multipoles_normal[0]) * r0**0
        for n, v in self.analysis_pos.multipoles_normal.items():
            self.multipoles_normal[n] = \
                self.analysis_pos.multipoles_normal[n] + \
                self.analysis_neg.multipoles_normal[n]
            self.multipoles_normal_relative[n] = \
                self.multipoles_normal[n] * (r0**n) / mm



    def run(self):
        """."""
        self.analysis_pos.files_run()
        self.analysis_neg.files_run()

    def calc_multipoles_kick(self, xmax,
                             multipoles_normal=None,
                             excluded_monomials=None):
        """."""
        if excluded_monomials is None:
            excluded_monomials = (0,)
        if multipoles_normal is None:
            multipoles_normal = self.multipoles_normal
        x = _np.linspace(-xmax, xmax, 101)
        y = _np.zeros(x.shape)
        for n, v in multipoles_normal.items():
            if n not in excluded_monomials:
                y += v * x**n
        brho, *_ = _util.beam_rigidity(self.beam_energy)
        y /= brho
        return y, x



def get_summary(dst, cur, pos):
    """."""
    data = (
        'Booster Dipoles Integrated Principal Multipoles\n'
        '================================================\n'
        '\n'
        'As calculated in {0:s}-half Runge-Kutta trajectory,\n'
        'defined by measured fieldmap with magnet excitated with current of'
        ' {1:s},\n'
        'corresponding to nominal particle energy of 3 GeV.\n'
        '\n').format(pos, cur)

    fmt = '{0:^10s} | {1:^11s} |  {2:^11s} | {3:^11s} | {4:^11s} |\n'
    data += fmt.format('Dipole', 'Angle [°]', 'Dint [T.m]', 'Gint [T]',
                       'Sint [T/m]')
    data += fmt.format('', '', '', '', '')

    fmt = ('{0:^10s} | {1:^+11.5f} |  {2:^+11.5f} | {3:^+11.5f} |'
           ' {4:^+11.5f} |\n')
    for i in range(4, 58):
        name = 'bd-{0:03d}'.format(i)
        fi = dst + '/' + name + '/M1/{0:s}/z-{1:s}/'.format(cur, pos)
        fname = './' + fi + cur + '.pkl'
        # print(fname)
        with open(fname, 'rb') as fi:
            config = _pic.load(fi)
        si = 1 if pos == 'positive' else -1
        multi = config.multipoles.normal_multipoles_integral
        theta = si*_np.arctan(config.traj.px[-1]/config.traj.pz[-1])*180/_np.pi
        data += fmt.format(name, theta, multi[0], multi[1], multi[2])

    print(data)
    with open(dst + '/README-{0:s}-Z{1:s}.md'.format(cur, pos), 'w') as fi:
        fi.write(data)


def get_new_energy(dst, cur):
    """."""
    theta = _np.zeros(54)
    for i in range(4, 58):
        for pos in ['positive', 'negative']:
            fi = dst + '/bd-{0:03d}/M1/' + cur + '/z-{1:s}/'.format(i, pos)
            with open(fi + cur + '.pkl', 'rb') as fi:
                config = _pic.load(fi)
            si = 1 if pos == 'positive' else -1
            theta[i-4] += \
                si*_np.arctan(config.traj.px[-1]/config.traj.pz[-1])*180/_np.pi

    print(theta)
    print('New Energy = {0:7.5f} GeV'.format(theta.mean()/-7.2 * 3))


def print_help():
    """."""
    print(_help)


def main():
    """."""
    n = len(_sys.argv)
    if n > 1 and 'summary' in _sys.argv[1]:
        dst = _sys.argv[2] if n > 2 else 'x0-9p1013mm'
        cur = _sys.argv[3] if n > 3 else '0991p63A'
        pos = _sys.argv[4] if n > 4 else 'positive'
        get_summary(dst, cur, pos)
    elif n > 1 and 'energy' in _sys.argv[1]:
        dst = _sys.argv[2] if n > 2 else 'x0-9p1013mm'
        cur = _sys.argv[3] if n > 3 else '0991p63A'
        get_new_energy(dst, cur)
    elif n > 1 and 'help' in _sys.argv[1]:
        print_help()
    else:
        print_help()


if __name__ == '__main__':
    main()

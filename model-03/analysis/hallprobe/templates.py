"""Fieldmap analysis File Templates."""

rawfield = """
# ==========================
# fma_rawfield.py input file
# Date: TIMESTAMP
# Accelerator Physics LNLS
# ==========================

# --- Summary ---
#
# this is the input file for fac-fma-rawfield.py script
# this script reads a fieldmap from a 3D magnet model, stores it
# for latter analysis and prints and plots basic information on the
# field map. It is used to quickly inspect the fieldmap


# --- Input parameters ---

# each analysis has an identity label used for naming output files

  config_label             'CONFIG_NAME'


# the next parameter specifies the type of magnet to be analysed.
# each type may have its own particular algorithms to be applied

  magnet_type              'dipole'


# the full name of the file that contains the field map

  fmap_filename            'FIELDMAP_FNAME'

# Runge-Kutta algorithm used for the integration of the eqs. of motion needs to know
# what to do when trajectory reaches the fieldmap bounds. It will either extrapolate the field
# along the longitudinal (z) direction or consider it to have vanished. This is controlled with
# the parameter below. Bear in mind that the calculation of extrapolation coefficients is very
# time-consuming currently. As for the transverse directions (x and y), the RK algorithm will
# generate exceptions.

  fmap_extrapolation_flag  False

"""

trajectory = """
# ==========================
# fma_rawfield.py input file
# Date: TIMESTAMP
# Accelerator Physics LNLS
# ==========================

# --- Summary ---
#
# This is the input file for trajectory calculation based on a given
# fieldmap which is performed with the script 'fac-fma-trajectory.py'
# A controllable fixed-size Runge-Kutta algorithm is used to integrate
# the equations of motion of a single electron in the presence of
# the magnetic field as defined in the fieldmap.
#
# The implemented equations of motion are not approximated. Provided
# a sufficiently fine RK step is chosen, this scripts may be used to
# accurately obtain the trajectory of the electron with arbitrary energy
#
# Runge-Kutta algorithm used for the integration of the eqs. of motion needs to know
# what to do when trajectory reaches the fieldmap bounds. It will either extrapolate the field
# along the longitudinal (z) direction or consider it to have vanished.
# As for the transverse directions (x and y), the RK algorithm will
# generate exceptions.


# --- Input parameters ---

# each analysis has an identity label used for naming output files

  config_label             	'CONFIG_NAME'


# beam energy

  beam_energy                     BEAM_ENERGY     # [GeV]


# A trajectory can also be read from file. This is useful when the fieldmap of
# 3D models with errors are being analysed. In this case we want to use as reference
# trajectory a trajectory that was calculated from the 3D model without errors and
# saved to file. If parameter 'traj_load_filename' is set to 'None' then a new
# reference trajectory with be calculated with RK on the given fieldmap.

  traj_load_filename              None


# If parameter 'traj_is_reference_traj' is set to True the algorithm will rescale the
# fieldmap so that the total trajectory deflection will exactly match the nominal deflection

  traj_is_reference_traj          False
  model_nominal_angle             7.2                           # [deg] model nominal deflection angle of the magnet

# There is the option to restrain the trajectory to the midplane (y = 0 mm) of the magnet

  traj_force_midplane_flag        True


# There is the option to serach for a initial rx position that will result in a trajectory that
# is centered in the good-field region of the magnet (around rx == 0)

  traj_center_sagitta_flag        False


# The RK algorithm always integrates the trajectory from the center of the magnet (z = s = 0 mm)
# The limits of the RK integration may be specified in various ways:
# If only 'traj_rk_s_step' is given then the algorithm will integrate until
# the z coordinate of the particle reaches the fieldmap bound.

  traj_init_rx                    RX_INIT                       # [mm] init_rx at z = s = 0 mm (center of magnet)
  traj_rk_s_step                  S_STEP                        # [mm]
  traj_rk_length                  None                          # [mm]
  traj_rk_nrpts                   None


# whether to save trajectory to an ASCII file

  traj_save                       True
"""

multipoles = """
# ==========================
# fma_rawfield.py input file
# Date: TIMESTAMP
# Accelerator Physics LNLS
# ==========================

# --- Summary ---
#
# this is the input file for the 'fac-fma-multipoles.py' script
# this script calculates the multipoles around the reference trajectory.


# --- Input parameters ---

# each analysis has an identity label used for naming output files

  config_label                      'CONFIG_NAME'


# the multipoles (m1,m2,...) to be calculated are defined by a list of position x exponents (n1,n2,...):
# By = m1 * x^n1 + m2 * x^n2 + ...

  multipoles_normal_field_fitting_monomials      (0,1,2,3,4,5,6)                 # monomials to be included in the polynomial fit of multipoles
  multipoles_skew_field_fitting_monomials        ()

# grid of perpendicular points around each point of the reference trajectory for the polynomial fit of By and Bx

  multipoles_perpendicular_grid     np.linspace(-12,12,65)          # grid of points on perpendicular line to ref trajectory [mm]

# after multipole coeffs are calculated, their normalized strengths at perp. position r0 are calculated (as defined in tracy)

  multipoles_r0                     17.5                             # [mm] horizontal position at which polynomial fields are calculated relative to the principal multipole
  normalization_monomial            0
  normalization_is_skew             False

# integrated residual field (converted to kick angle) calculated from fitted multipoles and
# from integrated fieldmap are compared. The parameter below lists the monomials which are
# supposed to define the main field. The rest makes up for the residual field

  normal_multipoles_main_monomials         (0,1,2)
  skew_multipoles_main_monomials           ()
"""

model = """
# ==========================
# fma_rawfield.py input file
# Date: 2018-07-20
# Accelerator Physics LNLS
# ==========================

# --- Summary ---
#
# This script integrates fitted multipoles at each segment of the hard-edge model

# --- Input parameters ---

# each analysis has an identity label used for naming output files

  config_label                      'CONFIG_NAME'


# list with lengths of model segments

   model_segmentation               (196, 192, 182, 10, 10, 13, 17, 20, 30, 50)
"""

help = """
NAME
       hallprobe.py - routines and libs to process fieldmap analysis

SYNOPSIS
       hallprobe.py [CMD] [ARGS]

DESCRIPTION
       The command options are

       help
       summary  [x0-9p1013mm|...] [current_label] [positive|negative]
       new-energy [x0-9p1013mm|...]
"""

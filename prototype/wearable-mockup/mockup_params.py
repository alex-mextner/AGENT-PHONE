"""Millimetres, X across / Y along forearm / Z above nominal dorsal skin.
Inert closed-position fit study; neither production packaging nor proven fit.
"""
MODULE_MM = (44.0, 92.0, 6.6)
TOP_Z, TRAY_BOTTOM_Z, FLOOR_Z, LID_BOTTOM_Z = 14.8, 8.2, 9.4, 12.6
BASE_BOTTOM_Z, BASE_TOP_Z = 1.4, 6.2  # deeper recess protects against fastener tolerances
FLANGE_BOTTOM_Z, FLANGE_TOP_Z = 6.2, 8.2
SCREW_XY = ((-12.0,-9.0), (-12.0,9.0), (12.0,-9.0), (12.0,9.0))
SCREW_LENGTH_MM, SCREW_HEAD_TOP_Z = 12.0, 14.6
SCREW_THREAD_DIA, SCREW_HEAD_DIA, CLEARANCE_DIA = 3.0, 5.6, 3.4
SCREW_CONE_DEPTH_MM = 1.3  # 90-degree cone; simplified thread envelope
NUT_AF, NUT_HEIGHT, NUT_TOP_Z = 5.5, 2.4, 4.9
NUT_POCKET_AF = 5.9
BOSS_RADIUS = 3.6
CUFF_THICKNESS, CUFF_CLEARANCE = 3.0, 2.5
CUFF_ROOT_WIDTH, CUFF_MIDDLE_WIDTH, CUFF_TIP_WIDTH = 12.0, 28.0, 12.0
CUFF_FRONT_Y, CUFF_END_ANGLE_DEG = -14.0, 125.0
PROFILES = {'slim': (52.0,36.0), 'average': (58.0,42.0), 'large': (64.0,46.0)}
DENSITY_G_CM3 = {'PLA':1.24, 'PETG':1.27, 'TPU':1.21, 'steel':7.85}
BALLAST_THICKNESS = 2.5
BALLAST_BOTTOM_Z = 9.5
PRINT_BED_MM = 220.0

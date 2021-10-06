import numpy as np
import matplotlib.pyplot as plt
import ast2000tools.utils as utils
# from ast2000tools.solar_system import SolarSystem
import ast2000tools.constants as const
from ast2000tools.space_mission import SpaceMission

seed = utils.get_seed('antonabr')
# system = SolarSystem(seed)
mission = SpaceMission(seed)

star_angles = mission.star_direction_angles
star_doppler_shifts = mission.star_doppler_shifts_at_sun

# star1_angle = mission.star_direction_angles[0]
# star2_angle = mission.star_direction_angles[1]
#
# star1_Doppler_shift = mission.star_doppler_shifts_at_sun[0]
# star2_Doppler_shift = mission.star_doppler_shifts_at_sun[1]

c = const.c # m/s
H_alpha = 656.3 # nm
deg_to_rad = np.pi / 180

def v_rad(delta_lambda, lambda_0 = H_alpha):
    return c * delta_lambda / lambda_0

sun_vr_relative_to_star1 = v_rad(star_doppler_shifts[0])
sun_vr_relative_to_star2 = v_rad(star_doppler_shifts[1])

# print(sun_vr_relative_to_star1, sun_vr_relative_to_star2)
'''
-7520.367522664845 -6898.527015994594
'''

spacecraft_phi_veloity = np.array([sun_vr_relative_to_star1, sun_vr_relative_to_star2]) # delta_lambda = 0 => spacecraft har the same v_rad as ref. stars

def phi_to_xy_transformation(vector):
    phi_1 = star_angles[0] * deg_to_rad
    phi_2 = star_angles[1] * deg_to_rad
    transformation_array = np.array([[np.sin(phi_2), -np.sin(phi_1)], [-np.cos(phi_2), np.cos(phi_1)]])
    scaler = 1 / np.sin(phi_2 - phi_1)

    return scaler * np.matmul(transformation_array, vector)

# print(phi_to_xy_transformation(spacecraft_phi_veloity))
'''
[ 1894.28538153 14163.36931175]
'''

def v_rad_spacecraft(delta_lambda, lambda_0 = H_alpha):
    v_rad_phi = c * delta_lambda / lambda_0
    

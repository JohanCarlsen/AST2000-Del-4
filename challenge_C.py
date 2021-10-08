'''
EGEN KODE
'''

import numpy as np
import ast2000tools.utils as utils
import ast2000tools.constants as const
from ast2000tools.space_mission import SpaceMission

seed = utils.get_seed('antonabr')
mission = SpaceMission(seed)

star_angles = mission.star_direction_angles
star_doppler_shifts = mission.star_doppler_shifts_at_sun

# print(star_angles)
'''
(320.6272467322133, 201.24860053586167)
'''

# print(star_doppler_shifts)
'''
(-0.016463446872719317, -0.015102125352990874)
'''

c = const.c_AU_pr_yr    # AU/yr
H_alpha = 656.3         # nm
deg_to_rad = np.pi / 180

def v_rad(delta_lambda, lambda_0 = H_alpha):
    '''
    Doppler effect
    delta lambda/lambda_0 = v_r/c
    '''
    v_r = c * delta_lambda / lambda_0
    return v_r

sun_vr_relative_to_star1 = v_rad(star_doppler_shifts[0])    # radial velocity to home star relative to ref. stars
sun_vr_relative_to_star2 = v_rad(star_doppler_shifts[1])

# print(sun_vr_relative_to_star1, sun_vr_relative_to_star2)
'''
-1.5863853932186576 -1.4552111263067906
'''

spacecraft_phi_veloity = np.array([sun_vr_relative_to_star1, sun_vr_relative_to_star2]) # delta_lambda = 0 => spacecraft has the same v_rad as ref. stars

def phi_to_xy_transformation(vector):
    '''Coordinate transformation'''
    phi_1 = star_angles[0] * deg_to_rad
    phi_2 = star_angles[1] * deg_to_rad
    transformation_array = np.array([[np.sin(phi_2), -np.sin(phi_1)], [-np.cos(phi_2), np.cos(phi_1)]])
    scaler = 1 / np.sin(phi_2 - phi_1)

    return scaler * np.matmul(transformation_array, vector)

# print(np.array([0,0]) - phi_to_xy_transformation(spacecraft_phi_veloity))   # v_rel (home star system) = v_spacecraft (ref. star system) - v_homestar (ref. star system)
'''
[-0.3995904 -2.9876947]
'''

def v_rad_rel_home_star(delta_lambda_1, delta_lambda_2, lambda_0 = H_alpha):
    '''
    This function takes to delta lambdas and
    calculates the radial velocities in both
    phi-systems. Then transform into xy-system.
    '''
    v_rad_phi_1 = v_rad(delta_lambda_1)
    v_rad_phi_2 = v_rad(delta_lambda_2)
    v_rad_phi = np.array([v_rad_phi_1, v_rad_phi_2])
    star_vr_rel_to_sun = np.array([sun_vr_relative_to_star1, sun_vr_relative_to_star2])
    v_rad_minus_vrel_ref_stars = -(v_rad_phi - star_vr_rel_to_sun)          # i dont know why, but the minus sign gives me the right answer
    return phi_to_xy_transformation(v_rad_minus_vrel_ref_stars)

test = v_rad_rel_home_star(star_doppler_shifts[0],star_doppler_shifts[1])   # we know that if the craft has velocity 0 in xy-system, the doppler shifts must be the same for the craft as for our home star.
# print(test)
'''
[-0. -0.]
'''

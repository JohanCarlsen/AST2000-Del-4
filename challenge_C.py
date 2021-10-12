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
doppler_shifts_measured_at_sun = mission.star_doppler_shifts_at_sun

print(star_angles)
'''
(320.6272467322133, 201.24860053586167)
'''

print(doppler_shifts_measured_at_sun)
'''
(-0.016463446872719317, -0.015102125352990874)
'''

c = const.c_AU_pr_yr    # AU/yr
H_alpha = 656.3         # nm
deg_to_rad = np.pi / 180

# challenge C.1

def v_rad(delta_lambda, lambda_0 = H_alpha):
    '''
    Doppler effect
    Uses doppler shift as measured by reciever
    To find relative velocities with respect to
    the transmitter, the radial velocity changes
    direction, hence the minus sign
    '''
    v_r = c * -delta_lambda / lambda_0
    return v_r

# challenge C.2

sun_vr_rel_to_ref_stars = np.array([v_rad(doppler_shifts_measured_at_sun[0]), v_rad(doppler_shifts_measured_at_sun[1])])
sun_vr_relative_to_star1 = v_rad(doppler_shifts_measured_at_sun[0])    # radial velocity to home star relative to ref. stars
sun_vr_relative_to_star2 = v_rad(doppler_shifts_measured_at_sun[1])
print(sun_vr_rel_to_ref_stars[0], sun_vr_rel_to_ref_stars[1])

print('Our home stars radial velocities relative to the reference stars:', sun_vr_rel_to_ref_stars)
'''
Our home stars radial velocities relative to the reference stars: [1.58638539 1.45521113]
'''

# challenge C.3

delta_lambda = np.array([0,0])
craft_rad_vel_rel_to_ref_stars = np.array([v_rad(delta_lambda[0]), v_rad(delta_lambda[1])])    # delta_lambda = [0,0] => spacecraft has the same v_rad as ref. stars

print(f'Spacecrafts radial velocities relative to the reference stars when the doppler shifts={delta_lambda}:', craft_rad_vel_rel_to_ref_stars)
'''
Spacecrafts radial velocities relative to the reference stars when the doppler shifts=[0 0]: [0. 0.]
'''
craft_rad_vel_rel_to_sun = craft_rad_vel_rel_to_ref_stars - sun_vr_rel_to_ref_stars

print(f'Spacecrafts radial velocities relative to home star when the doppler shifts at reference stars={delta_lambda}:', craft_rad_vel_rel_to_sun)
'''
Spacecrafts radial velocities relative to home star when the doppler shifts at reference stars=[0 0]: [-1.58638539 -1.45521113]
'''

# challenge C.4

def phi_to_xy_transformation(vector):
    '''Coordinate transformation'''
    phi_1 = star_angles[0] * deg_to_rad
    phi_2 = star_angles[1] * deg_to_rad
    transformation_array = np.array([[np.sin(phi_2), -np.sin(phi_1)], [-np.cos(phi_2), np.cos(phi_1)]])
    scaler = 1 / np.sin(phi_2 - phi_1)

    return scaler * np.matmul(transformation_array, vector)

craft_rad_vel_rel_to_sun_xy_system = phi_to_xy_transformation(craft_rad_vel_rel_to_sun)

print('When we transfom the velocities from phi-system to xy-system, we get:', craft_rad_vel_rel_to_sun_xy_system)
'''
When we transfom the velocities from phi-system to xy-system, we get: [0.3995904 2.9876947]
'''

def v_rad_rel_home_star(delta_lambda_1, delta_lambda_2, lambda_0 = H_alpha):
    '''
    This function takes to delta lambdas and
    calculates the radial velocities in both
    phi-systems. Then transform into xy-system.
    '''
    rad_vel_phi_system = np.array([v_rad(delta_lambda_1), v_rad(delta_lambda_2)])
    rad_vel_rel_to_sun_phi_system = rad_vel_phi_system - sun_vr_rel_to_ref_stars

    return phi_to_xy_transformation(rad_vel_rel_to_sun_phi_system)

test = v_rad_rel_home_star(doppler_shifts_measured_at_sun[0],doppler_shifts_measured_at_sun[1])   # we know that if the craft has velocity 0 in xy-system, the doppler shifts must be the same for the craft as for our home star.

print(f'When the measured doppler shift is the same for our spacecraft as for our sun, we expect to get the velocities [0, 0]. We get:', test)
'''
When the measured doppler shift is the same for our spacecraft as for our sun, we expect to get the velocities [0, 0]. We get: [-0. -0.]
'''

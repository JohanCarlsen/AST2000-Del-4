'''
EGEN KODE og snarvei
'''

import numpy as np
import ast2000tools.utils as utils
import ast2000tools.constants as const
from ast2000tools.solar_system import SolarSystem
from ast2000tools.space_mission import SpaceMission
from ast2000tools.shortcuts import SpaceMissionShortcuts
from challenge_C import v_rad, phi_to_xy_transformation, v_rad_rel_home_star

seed = utils.get_seed('antonabr')
mission = SpaceMission(seed)

'''Shortcut'''
code_engine = 50557
code_launch = 25206
code_escape_trajectory = 14143

mission = SpaceMission(seed)
system = SolarSystem(seed)

shortcut = SpaceMissionShortcuts(mission, [code_engine, code_launch, code_escape_trajectory])

rocket_params = shortcut.compute_engine_performance(1e5 / (1e-6)**3, 5e3, 0.25 * 1e-6 ** 2)

Nbox = 2e30
total_rocket_params = np.array(rocket_params) * Nbox
thrust, mass_loss = total_rocket_params #N, kg / s

initial_fuel_mass = 1e20 # kg
Tlaunch = 500 # s
radius = system.radii[0] * 1e3 # m
R0 = system.initial_positions[:, 0] # AU
R0 = R0 + np.array([radius, 0]) * 6.68459e-12 # AU
T0 = 0 # yr

print("Respectively thrust and mass-loss from single rocket-engine-box:")
print(rocket_params)

mission.set_launch_parameters(thrust, mass_loss, initial_fuel_mass, Tlaunch, R0, T0)
mission.launch_rocket()
#mission.verify_launch_result("din rakett posisjon etter start")

print("Launch shortcut:")
print(shortcut.get_launch_results())
print("Escape trajectory shortcut:")

height_above_suface = 1e7 # m
direction = 90 # degrees wrt. x-axis
fuel_left = 1e4 # kg

shortcut.place_spacecraft_on_escape_trajectory(thrust, mass_loss, T0, height_above_suface, direction, fuel_left)
'''Shortcut end'''

print('---------------------------------')

'''EGEN KODE'''

def spacecraft_position(measured_distances, known_positions):
    '''Function to calculate position using triangulation'''
    r1, r2, r3 = [measured_distances[i] for i in range(1,-2,-1)]    # unpacks distances from craft to planets/home star in AU
    pos1, pos2 = [known_positions[:,i] for i in range(1,-1,-1)]     # unpacks positions for home planet and neighbor planet rel. to home star in AU
    pos3 = np.array([0,0])                                          # home star position is in the origin in AU

    x1, y1 = pos1
    x2, y2 = pos2
    x3, y3 = pos3
    '''
    The following constants are the results from
    the two solution equations we got from the three
    circle equations which will intersect at our position.
    '''
    A = -2*(x1 - x2)
    B = -2*(y1 - y2)
    C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = -2*(x1 - x3)
    E = -2*(y1 - y3)
    F = r1**2 - r3**2 - x1**2 + x3**2 - y1**2 + y3**2
    '''
    These are the solutions to the equations
    Ax+By=C
    Dx+Ey=F
    '''
    x = (C*E - B*F) / (A*E - B*D)   # x-position of the craft
    y = (A*F - C*D) / (A*E - B*D)   # y-position of the craft

    pos = np.array([x,y])           # in AU
    return pos

# mission.take_picture()
delta_lambda_1, delta_lambda_2 = mission.measure_star_doppler_shifts()

print('Measured doppler shifts:', mission.measure_star_doppler_shifts())
'''
Measured doppler shifts: (0.03702057888274662, 0.015453611179630155)
'''

craft_velocity = v_rad_rel_home_star(delta_lambda_1, delta_lambda_2)

print('Calculated velocity:', craft_velocity)
'''
Calculated velocity: [5.09629203e-16 8.12408017e+00]
'''

craft_position = spacecraft_position(mission.measure_distances(), system.initial_positions)

print('Calculated position:', craft_position)
'''
Calculated position: [1.85891332e+00 1.17687184e-04]
'''

craft_azimuthal_angle = 270 # here i used the program "part4_taskB.py" with img = sky_picture.png, which is the picture generated from the rockets camera


mission.verify_manual_orientation(craft_position, craft_velocity, craft_azimuthal_angle)
'''
Pointing angle after launch correctly calculated. Well done!
Velocity after launch correctly calculated. Well done!
Position after launch correctly calculated. Well done!
Your manually inferred orientation was satisfyingly calculated. Well done!
*** Achievement unlocked: Well-oriented! ***
'''

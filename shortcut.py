import ast2000tools.utils as utils
from ast2000tools.solar_system import SolarSystem
from ast2000tools.space_mission import SpaceMission
from ast2000tools.shortcuts import SpaceMissionShortcuts
import numpy as np

seed = 12497
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

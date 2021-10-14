from PIL import Image
import numpy as np
import ast2000tools.constants as const
import ast2000tools.utils as utils
from ast2000tools.solar_system import SolarSystem
from ast2000tools.space_mission import SpaceMission
import matplotlib.pyplot as plt
from numba import njit

"""
Egen kode !!!
Anton Brekke
"""

seed = utils.get_seed('antonabr')
system = SolarSystem(seed)
mission = SpaceMission(seed)

img0 = Image.open('sample0000.png') # Åpner sample-bildet
pixels = np.array(img0) # png til numpy-array
# print(pixels.dtype)   #uint8
shape = np.shape(img0)   # Shape av sample-bildet
# print(shape)
from_grad_to_rad = np.pi / 180      # Til konvertering mellom grader og radianer

at = 70 * from_grad_to_rad      # FOV a_theta
ap = 70 * from_grad_to_rad      # FOV a_phi
phi0 = 112.3 * from_grad_to_rad                        # 0 samme i grader og radianer, testbildet 1testpic laget på 43.2 grader
theta0 = 90 * from_grad_to_rad
# Max/min verdier for xy-grid
Xmax = 2*np.sin(ap/2) / (1 + np.cos(ap/2))
Ymax = 2*np.sin(at/2) / (1 + np.cos(at/2))
Xmin = -Xmax
Ymin = -Ymax
# Lager et meshgrid
I = np.linspace(Xmin, Xmax, 640)
J = np.linspace(Ymin, Ymax, 480)
X, Y = np.meshgrid(I, J, indexing='xy')
rho = np.sqrt(X**2 + Y**2)
beta = 2*np.arctan(rho/2)

# Laster inn 3D-kule-bildet
himmelkule = np.load('himmelkule.npy')

theta = theta0 - np.arcsin(np.cos(beta)*np.cos(theta0) + Y/rho*np.sin(beta)*np.sin(theta0)) # Polar angle
phi = phi0 + np.arctan(X*np.sin(beta) / (rho*np.sin(theta0)*np.cos(beta) - Y*np.cos(theta0)*np.sin(beta)))  # Azimuth-angle

# Lager først et bilde for å sjekke om det stemmer
pixel_array = np.zeros(shape, dtype=np.uint8)   # Må bruke samme dtype som sample-bildet (generelt for bilder)
for i in range(len(theta[:,0])):
    for j in range(len(theta[0,:])):
        pixel_index = mission.get_sky_image_pixel(theta[i,j], phi[i,j])     # Henter piksel-indeks via. polar og asimutal vinkel
        pixel_array[i,j,:] = himmelkule[pixel_index, 2:]            # Setter verdiene i pixel_array lik RGB-verdien til piksel i himmelkule

img2 = Image.fromarray(pixel_array[::-1, :, :])         # Bildet ble flippa så jeg flipper det tilbake her
img2.save('1testpic_taskB.png')     # Lagrer bildet

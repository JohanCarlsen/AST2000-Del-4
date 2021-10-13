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
Inneholder som vanlig blanding av norsk-engelsk kommentar ;)
"""

seed = utils.get_seed('antonabr')
system = SolarSystem(seed)
mission = SpaceMission(seed)

img = Image.open('1testpic_taskB.png') # Åpner sample-bildet
pixels = np.array(img, dtype=np.uint8) # png til numpy-array
# print(pixels.dtype)   #uint8
shape = np.shape(pixels)   # Shape av sample-bildet
print(shape)
print(img)      # Printer ut hva slags objekt det er
print(np.size(img))     # 640 x 480 størrelse
from_grad_to_rad = np.pi / 180      # Til konvertering mellom grader og radianer

"""
Lager en array som inneholder alle 360 bilder
generert tidligere så vi kun behøver å regne minste
kvadraters metode 1 gang. Bildene lastes inn i rekkefølge
1 - 359 for å spare oss for jobb med å finne vinkler senere.
"""
pix_360_array = np.zeros((360, *shape), dtype=np.uint8)     # Lager med samme dtype som pixels (uint8 = unsigned integers 8 bits)
# Henter inn alle relevante bilder lagret i mappen
for i in range(0, 360):
    pic_name = f'skyimage_{i}.png'
    pic = Image.open(pic_name)
    pix_360_array[i,:,:,:] = pic
# print(pix_360_array)

"""
Bruker minste kvadraters metode for å finne hvilket bilde fra referansebildene
lastet inn tidligere som passer best med RGB-verdiene til bildet som ble tatt.
Referansebildene er lagt inn i rekkefølge etter grad, slik at indeksen vi finner i sq
som har minste verdi også er lik graden phi bildet er tatt i.
"""
def least_squares(image):
    """
    Minste kvadraters metode på RGB (axis=3), summerer alle pikslene
    i gridet og deler på gridstørrelsen for å få fornuftige tall
    (et slags snitt av RGB verdier i hele bildet)
    """
    sq = np.sum(np.sum(np.sum(image[None,:,:,:] - pix_360_array, axis=3, dtype=np.uint8)**2, axis=1), axis=1) / (640*480)  # Akser 3 og 2 faller til akse 1 etter sum. Akse 0 er alle bildene
    # print(sq)
    phi_new = np.where(sq==np.min(sq))[0][0]        # Husk : theta = 90deg.
    # Plotter minste kvadratene
    deg = np.linspace(0, 359, 360)
    # plt.style.use('seaborn-whitegrid')
    plt.plot(deg, sq, 'royalblue')
    plt.grid(True, linestyle=':')
    plt.xlabel(r'$\phi$ [deg]', fontsize=16, weight='bold')
    plt.ylabel(r'$\Delta$ (least squares)', fontsize=14, weight='bold')
    plt.show()
    return phi_new

phi_new = least_squares(pixels)
print(phi_new)

# Fra terminal
"""
(480, 640, 3)
<PIL.PngImagePlugin.PngImageFile image mode=RGB size=640x480 at 0x1105B8E0>
(640, 480)
112
"""

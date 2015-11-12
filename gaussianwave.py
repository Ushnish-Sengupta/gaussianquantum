import numpy as np
import matplotlib.pyplot as plt
import cmath as cm
import math as mt
import scipy.constants as sp
from math import pi
from matplotlib import animation

plt.rcParams['animation.ffmpeg_path']='C:\\Program Files\\ImageMagick-6.9.2-Q16\\ffmpeg.exe'

length = 40     # plotting region
vgl = 1
vgr = -1        # phase velocities
sigxl = 1
sigxr = 1          # spatial spread of psi
sigkl = 1/(2*sigxl)
sigkr = 1/(2*sigxr) # momentum spread
omesigl = 1/(2*(sigxl)**2)
omesigr = 1/(2*(sigxr)**2)
kl0 = vgl
kr0 = vgr   # wave numbers
locl0 = 3
locr0 = 37  # starting location of left and right packets


loc = np.arange(0., length, (length-0)/1000)
probden = np.arange(0., length, (length-0)/1000)    # probability density

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, length), ylim=(0, 0.5))
line, = ax.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

def animate(t):
    for i in range(len(loc)):
        prefl = 1/(cm.sqrt(cm.sqrt(2*sp.pi)*sigxl)*cm.sqrt(1+omesigl*t*1j))      
        prefr = 1/(cm.sqrt(cm.sqrt(2*sp.pi)*sigxr)*cm.sqrt(1+omesigr*t*1j))      # prefactor for gaussian
        
        psi1 = prefl*cm.exp((kl0*(loc[i]-locl0)-omesigl*t)*1j)*cm.exp(-(((loc[i]-locl0)-vgl*t)**2)/(4*sigxl*sigxl*(1+omesigl*t*1j)))
        psi2 = prefr*cm.exp((kr0*(loc[i]-locr0)-omesigr*t)*1j)*cm.exp(-(((loc[i]-locr0)-vgr*t)**2)/(4*sigxr*sigxr*(1+omesigr*t*1j)))
        psi = psi1 - psi2   # superposition
        probden[i] = (abs(psi))**2
    line.set_data(loc, probden)
    return line,

anim = animation.FuncAnimation(fig, animate, np.arange(0, 30, 0.1), init_func=init,
                               interval=0.1, blit=True)     # specify time range and stepping
mywriter = animation.FFMpegWriter()
anim.save('mymovie.mp4',writer=mywriter)
plt.ylabel('WAVE FUNCTION')
plt.xlabel('LOCATION IN a.u.')
plt.show()

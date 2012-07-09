"""
Calculate power distribution of laser scanning photo-activation device

Laser beam symbols used are from the beam power formula:
[1] en.wikipedia.org/wiki/Gaussian_beam#Power_through_an_aperture

References:
[2] radiantzemax.com/kb-en/Goto50125.aspx
[3] leica-microsystems.com/products/light-microscopes/accessories/objectives/
[4] en.wikipedia.org/wiki/Beam_diameter#D4.CF.83_or_second_moment_width
[5] en.wikipedia.org/wiki/Normal_distribution

Theory contributors in alphabetical order:
Browne, M. (Andor Technology)
Karunarathne, A. (Washington University in St. Louis)
Magidson, V. (Wadsworth Institute, NYSDOH)

Code Author:
Nanda, P. (Andor Technology)
"""

from math import pi, e
from numpy import sqrt, ogrid, hypot, zeros, array
import iqtools.mplot # must import this before pylab
from pylab import Figure, axes
from matplotlib.transforms import Bbox


## Create the round laser beam profile at the specimen plane

# Gaussian laser beam power (micro-Watts) at back focal plane, Symbol: Ps
# Measured by user's PD-300 laser meter using single pixel FRAP
Ps = 5

To = 0.84 # Percent transmission through above objective at 445nm 
Tm = 0.8 # Percent transmission through media, etc (estimated)
# Gaussian laser beam power (micro-Watts), Symbol: Po
Po = Ps * To * Tm

# FWHM Beam diameter / waist size (microns) at objective, Symbol: Wo
# Measured at objective specimen plane using FRAPPA slide
Wo_FWHM = 0.8

# Convert FWHM to 1/e^2 [2]
Wo = Wo_FWHM * 0.8493218 * 2

camera_pixel = 16 # (microns) e2v CCD97 pixel
mag_camera_tube_lens = 1.2
mag_objective = 63 # Objective Magnification of Leica 63x 1.4NA PlanApo 11506192 [3]
# Pixel calibration (microns / pixel)
cal = camera_pixel / float(mag_objective * mag_camera_tube_lens)

# Beam axis pixel length on camera (pixels), Symbol: px_len
# Wo for a single mode beam is 4 sigma wide [4]
px_len_2sig = Wo / cal
# Extend the beam diameter out to 6 sigma to contain 99% of Po
px_len = (6 / 4.) * px_len_2sig

px_fit = int(px_len) / px_len
px_to_edge = int(3 / px_fit)
edge = px_fit * px_to_edge
steps = int(px_len / px_fit)
#x = linspace(-edge, edge, steps)  # keep for debugging 1D construction

# Map 1D arrays radially
x, y = ogrid[-edge:edge:steps*1j,
             -edge:edge:steps*1j]
z = hypot(x,y)

# Create 2D gaussian beam profile
def norm(x, mean=0, sigma=1):
    """
    Returns single value from Gaussian / Normal distribution curve [5]
    """
    return (1/(sigma * sqrt(2 * pi))) * e ** (-0.5 * ((x - mean) / sigma) ** 2)

beam_profile = norm(z)

# norm() gives a 1D probability distribution, the area of which is 1.  The 2D
# beam profile thus needs to be re-normalized back to 1, for it to be
# multiplied by the Po scalar, obj_mag^2, and transmission losses
beam_profile /= beam_profile.sum()
beam_profile *= Po


## Setup ROI

w = 10 # pixels
h = 10 # pixels
length = x.shape[0]  # length in pixels of beam_profile square
x = w + length - length % 2
y = h + length - length % 2
roi = zeros((x,y))
row = zeros((x,length))


## Laser beam tiles ROI with overlap

# Using these two for loops below is an accurate, but brute-force way to
# create the tiling with overlap data.  Using for loops on numpy arrays is 
# bad practise.  It would be better to accomplish this mathematically with:
# 1.  Convolution, or
# 2.  Cross multiplication in Fourier space
for i in range(w):
    row[i:length+i,0:length] += beam_profile
for i in range(h):
    roi[0:y,i:length+i] += row

## Show results

# Area calculation
w_um = w * cal
h_um = h * cal
x_um = x * cal
y_um = y * cal
actual_area = x_um * y_um
drawn_area = w_um * h_um

# Power calculation
peak_pixel_power = roi.max() # uW
actual_power = roi.sum() # uW
drawn_power = roi[length/2:w+length/2,length/2:h+length/2].sum()
density_drawn_power = drawn_power / (drawn_area / 1000**2) # uW/mm^2

# Energy calculation
dwell_time = 80  # micro-seconds
repeats = 1
peak_pixel_energy = roi.max() * dwell_time * repeats / 1000 # uJ
actual_energy = actual_power * dwell_time * repeats / 1000 # uJ
drawn_energy = drawn_power * dwell_time * repeats / 1000 # uJ
density_drawn_energy = drawn_energy / (drawn_area / 1000**2) # uJ/mm^2

print('Laser Beam at Back Focal Plane-')
print('Measured Power: {0:3.0f} uW'.format(Ps))

print('')
print('Laser Beam at Objective Specimen Plane-')
print('Calculated Power: {0:3.0f} uW'.format(Po))
print('Measured Width: {0:1.1f} um, '.format(Wo_FWHM) + 'in FWHM')

print('')
print('Beam Profile Pixelation at Back Focal Plane-')
print('Calibration: {0:1.3f} um/pixel'.format(cal))
print('Size: {0} x {1} pixels, '.format(beam_profile.shape[0],
                                        beam_profile.shape[1]) +
      'covering 3 standard deviations')
print('<Plotting power of beam profile>')

fig = Figure()
beam_plot = fig.add_subplot(
    121,
    title='Single point\n laser beam profile\n at specimen plane (uW)',
    xlabel='pixel',
    ylabel='pixel',
)
axes_image = beam_plot.imshow(beam_profile, interpolation='nearest')
fig.colorbar(axes_image)

print('')
print('Region of Interest-')
print('Drawn Size: {0} x {1} pixels'.format(w, h) +\
      ' or {0:1.2f} x {1:1.2f} um'.format(w_um, h_um))
print('Drawn Area: {0:1.2f} um^2'.format(drawn_area))
print('...but due to edge spill over from laser raster scan...')
# FIXME: Actual Size should be based on something like FWHM or 1/e^2 (2 stddev)
print('Actual Size: {0} x {1} pixels'.format(x, y) +\
      ' or {0:1.2f} x {1:1.2f} um'.format(x_um, y_um) +\
      ', to 3 standard deviations')
print('Actual Area: {0:1.2f} um^2'.format(actual_area) +\
      ', to 3 standard deviations')

print('')
print('Power at Objective Specimen Plane-')
print('Average Power: ' +\
      '{0:3.1f} W/mm^2 over Drawn Area'.format(density_drawn_power / 1e6))
print('<Plotting power around ROI>')

roi_plot = fig.add_subplot(
    122,
    title='{0}x{0} pixel ROI\n laser spread\n at specimen plane (uW)'.format(w, h),
    xlabel='microns',
    ylabel='microns',
)
axes_image = roi_plot.imshow(roi,
                             extent=[-w_um, x_um, -h_um, y_um],
                             interpolation='nearest')
fig.colorbar(axes_image)
roi_plot.plot([0,0,w_um,w_um,0], [0,h_um,h_um,0,0],'b-', label='ROI', linewidth=2)
#roi_plot.annotate('ROI', (0,0))
roi_plot.legend()

print('')
print('Energy at Objective Specimen Plane-')
print('Dwell time: {0} us'.format(dwell_time))
print('Repeats: {0}'.format(repeats))
print('Average Energy: ' +\
      '{0:3.1f} J/mm^2 over Drawn Area'.format(density_drawn_energy / 1e6))

iqtools.mplot.showFigure(fig)
Power Density calculator of laser scanning device
=================================================

The standard performance measurement of illuminating a specimen on a microscope is measuring power density in mW/mm<sup>2</sup> or mW/cm<sup>2</sup> at the specimen plane.  If the specimen area is illuminated evenly, it possible to ignore laser beam shape altogether, and just calculate power density as:

![equation](http://latex.codecogs.com/gif.latex?P_%7Bdensity%7D%3D%5Cfrac%7BP_%7Bobjective%7D%7D%7BArea%7D)

However, with small laser scanned regions, the laser Gaussian beam shape creates edge artifacts or delivers lower power in a circular distribution.  This script was written for this possibility.  Below is the output for laser illuminating a 10 x 10 pixel region of interest (ROI)


Example Output
--------------
<img src="https://github.com/downloads/omsai/microscope-optical-input/figure.png"
 alt="Output Figure" title="Laser beam profiles" />
```
>>> 
Running script: 'C:\Documents and Settings\p.nanda\Desktop\WUSTL\raster_energy_roi.py'
Laser Beam at Back Focal Plane-
Measured Power:   5 uW

Laser Beam at Objective Specimen Plane-
Calculated Power:   3 uW
Measured Width: 0.8 um, in FWHM

Beam Profile Pixelation at Back Focal Plane-
Calibration: 0.212 um/pixel
Size: 10 x 10 pixels, covering 3 standard deviations
<Plotting power of beam profile>

Region of Interest-
Drawn Size: 10 x 10 pixels or 2.12 x 2.12 um
Drawn Area: 4.48 um^2
...but due to edge spill over from laser raster scan...
Actual Size: 20 x 20 pixels or 4.23 x 4.23 um, to 3 standard deviations
Actual Area: 17.92 um^2, to 3 standard deviations

Power at Objective Specimen Plane-
Average Energy: 56.8 W/mm^2 over Drawn Area
<Plotting power around ROI>

Energy at Objective Specimen Plane-
Dwell time: 80 us
Repeats: 1
Average Energy: 4.5 J/mm^2 over Drawn Area
>>> 
```


Usage
-----
These variables need to be hand edited in the Python script:
*  `Ps` power source - measurement of the optical input laser beam at the microscope nose piece without the objective
*  `M` objective magnification
*  `To` percent transmission of laser wavelength by objective
*  `Wo_FWHM` optical input laser beam size measured at specimen plane using uniform fluorescent ehidium bromide slide
*  `camera_pixel`
*  `mag_camera_tube_lens`
*  `w` ROI pixel width
*  `h` ROI pixel height

These variables yield the corresponding energy density:
*  `dwell_time` laser beam parameter
*  `repeats` laser beam parameter
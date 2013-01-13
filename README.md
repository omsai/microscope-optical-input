Power Density calculator of laser scanning device
=================================================

The standard performance measurement of illuminating a specimen on a microscope is measuring power density in mW/mm<sup>2</sup> or mW/cm<sup>2</sup> at the specimen plane.  If the specimen area is illuminated evenly, it possible to ignore laser beam shape altogether, and just calculate power density as:

![equation](http://latex.codecogs.com/gif.latex?P_%7Bdensity%7D%3D%5Cfrac%7BP_%7Bobjective%7D%7D%7BArea%7D)

However, with small laser scanned regions, the laser Gaussian beam shape creates edge artifacts or delivers lower power in a circular distribution.  This script was written for this possibility.  Below is the output for laser illuminating a 14 x 14 pixel region of interest (ROI)


Example Output
--------------
<img src="https://github.com/downloads/omsai/microscope-optical-input/figure.png"
 alt="Output Figure" title="Laser beam profiles" />
<img src="https://github.com/downloads/omsai/microscope-optical-input/line_figure.png"
 alt="Output Line Figure" title="Center cross section of optical input" />
```
>>> 
Running script: u'C:\Documents and Settings\p.nanda\My Documents\GitHub\microscope-optical-input\raster.py'
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
Drawn Size: 14 x 14 pixels or 2.96 x 2.96 um
Drawn Area: 8.78 um^2
...but due to edge spill over from laser raster scan...
Actual Size: 24 x 24 pixels or 5.08 x 5.08 um, to 3 standard deviations
Actual Area: 25.80 um^2, to 3 standard deviations

Power at Objective Specimen Plane-
Average Power: 66.7 W/mm^2 over Drawn Area
<Plotting power around ROI>

Energy at Objective Specimen Plane-
Dwell time: 80 us
Repeats: 1
Average Energy: 5.3 J/mm^2 over Drawn Area

<Plotting center cross section across ROI>

<Saving power around ROI to file>
>>> 
```


Usage
-----
These sets of variables need to be hand edited in the Python script:

Measurements:
*  `Ps` power source - measurement of the optical input laser beam at the microscope nose piece without the objective
*  `Wo_FWHM` optical input laser beam size measured at specimen plane using a uniform fluorescent ethidium bromide slide

Experimental parameters:
*  `mag_objective`
*  `w` ROI pixel width
*  `h` ROI pixel height
*  `dwell_time` laser beam parameter
*  `repeats` laser beam parameter

Optical Specifications:
*  `To` percent transmission of laser wavelength by objective
*  `camera_pixel`
*  `mag_camera_tube_lens`

# ocam
ocam: omnidirectional project points

This is purely numpy implementation of the projection functions of the Scaramuzza's  Omnidirectional Camera.

# Installation

Clone the repsitory and install
```
https://github.com/Chris10M/ocamcalib_python.git
cd ocamcalib_python
python -m pip install .                  
```

## Optional Dependacies

The conversion scripts for MATLAB intrinsics to JSON intrinsics and JSON to MATLAB intrinsics require MATLAB and [MATLAB Engine API for Python](https://de.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html).

**Tested with MATLAB R2023a**


# Usage
## Command Line
```
convert_intrinsics_to_matlab_cli path/to/fisheye_intrincis.json # output: path/to/fisheye_intrincis.mat
convert_matlab_to_intrincis_cli path/to/fisheye_intrincis.mat # output: path/to/fisheye_intrincis.json
```

## Minimal usage script
```
import ocam
import numpy as np

# Specify the path to the camera calibration JSON file
ocam_calib_json = 'intrinsics.json'

# Load the camera calibration model from the JSON file
ocam_calib_model = ocam.to_ocam_model(ocam_calib_json)

# Generate random 3D points (replace this with your actual 3D points)
num_points = 10  # Number of 3D points
points3D = np.random.rand(num_points, 1, 3)  # Random 3D points with x, y, z coordinates - Nx1x3

# Project the 3D points into 2D points using the camera calibration parameters
points2D = ocam.world2cam_np(points3D, ocam_calib_model) # points2D - Nx1x2

# Print the resulting 2D points
print("Projected 2D points:")
print(points2D)
```

The intrinsics.json has the following format,
```
{
    "pol": [161.14670546203945, 0, -0.00258314253679925, 6.035124622290237e-06, -2.5573236046748687e-08],
    "width": 640,
    "height": 480,
    "xc": 321.3651091048847,
    "yc": 236.25516320600983,
    "c": 1.0,
    "d": 0.0,
    "e": 0.0,
    "invpol": [246.60052640819538, -144.4605008632319, -6.62349373938239, -18.73714768763381, 14.831092227950778, 2.7995346430010786, 0.22537325854641585, -4.961875735767433, 1.7473552065804472]
}
``` 
the **invpol** in computed in *ocam.to_ocam_model* function.

### More examples:

Check out [example.py](./example.py) for more examples.


# Citations
If you find this code useful for research, consider citing:

* Original [Omnidirectional camera](https://link.springer.com/referenceworkentry/10.1007/978-0-387-31439-6_488) publication, 
```
@article{scaramuzza2014omnidirectional,
  title={Omnidirectional camera},
  author={Scaramuzza, Davide and Ikeuchi, Katsushi},
  year={2014},
  publisher={Springer US}
}
```
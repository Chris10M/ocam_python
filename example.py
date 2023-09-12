import ocam
import numpy as np
import json

# Generate random 3D points (replace this with your actual 3D points)
num_points = 10  # Number of 3D points
points3D = np.random.rand(num_points, 1, 3)  # Random 3D points with x, y, z coordinates - Nx1x3

# Load camera calibration parameters from a MATLAB file
ocam_calib_mat = 'intrinsics.mat'
ocam_calib_mat_model = ocam.load_matlab_intrinsics(ocam_calib_mat)

# Project 3D points to 2D using MATLAB-calibrated intrinsics
matlab_points2D = ocam.project_fisheye_points(points3D, ocam_calib_mat_model) # Nx1x2

# Convert MATLAB-calibrated intrinsics to a JSON format
ocam_calib_dict = ocam.convert_matlab_to_intrincis(ocam_calib_mat)

# Save the intrinsics to a JSON file
with open('intrinsics.json', 'w') as f:
    json.dump(ocam_calib_dict, f, indent=4)


# Load the camera calibration model from the JSON file
ocam_calib_json = 'intrinsics.json'
ocam_calib_model = ocam.to_ocam_model(ocam_calib_json) # or ocam_calib_model = ocam.to_ocam_model(ocam_calib_dict)


# Project the 3D points into 2D points using the camera calibration parameters
points2D = ocam.world2cam_np(points3D, ocam_calib_model)

# Print the resulting 2D points
print("Projected 2D points:")
print(points2D)

# Print the resulting 2D points from MATLAB
print("Projected 2D points from MATLAB:")
print(matlab_points2D)

# Project 3D points to 2D individually and print
print("Projected 2D points (individual):")
for point3d in points3D:
    point2d = ocam.world2cam(point3d, ocam_calib_model)
    print(point2d)


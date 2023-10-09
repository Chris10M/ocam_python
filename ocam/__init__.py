try:
    from .matlab_wrapper import load_matlab_intrinsics, project_fisheye_points, convert_intrinsics_to_matlab, convert_matlab_to_intrincis
except ImportError:
    def load_matlab_intrinsics(*args, **kwargs):
        raise NotImplementedError('Could not import matlab engine. Make sure Matlab is installed and MATLAB engine API for Python.')
    
    def project_fisheye_points(*args, **kwargs):
        raise NotImplementedError('Could not import matlab engine. Make sure Matlab is installed and MATLAB engine API for Python.')

    def convert_intrinsics_to_matlab(*args, **kwargs):
        raise NotImplementedError('Could not import matlab engine. Make sure Matlab is installed and MATLAB engine API for Python.')

    def convert_matlab_to_intrincis(*args, **kwargs):
        raise NotImplementedError('Could not import matlab engine. Make sure Matlab is installed and MATLAB engine API for Python.')

    print('Could not import matlab engine. Some functions will not work.')
    
from .world2cam_fast import world2cam_fast
from .world2cam import world2cam, world2cam_np, world2cam_torch
from .preprocess_ocam_json import to_ocam_model


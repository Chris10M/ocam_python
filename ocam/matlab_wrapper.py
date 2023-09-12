import numpy as np
import matlab.engine
import matlab
import json
import argparse

from preprocess_ocam_json import to_ocam_model

eng = matlab.engine.start_matlab()

def convert_intrinsics_to_matlab(ocam_model):
    xc = ocam_model['xc']
    yc = ocam_model['yc']
    width = ocam_model['width']
    height = ocam_model['height']
    c = ocam_model['c']
    d = ocam_model['d']
    e = ocam_model['e']
    pol = ocam_model['pol']

    mappingCoeffs = np.array([pol[0], pol[2], pol[3], pol[4]])
    imageSize = np.array([height, width])
    distortionCenter = np.array([xc, yc])
    stretchMatrix = np.array([[c, d], [e, 1]])

    mappingCoeffs = matlab.double(mappingCoeffs.astype(dtype=np.double)) 
    imageSize = matlab.double(imageSize.astype(dtype=np.double)) 
    distortionCenter = matlab.double(distortionCenter.astype(dtype=np.double)) 
    stretchMatrix = matlab.double(stretchMatrix.astype(dtype=np.double)) 


    intrinsics = eng.fisheyeIntrinsics(mappingCoeffs,imageSize,distortionCenter, stretchMatrix)

    return intrinsics

def convert_matlab_to_intrincis(intrinsics):
    if isinstance(intrinsics, str):
        content = eng.load(intrinsics, nargout=1)

        if eng.isfield(content, 'fisheye_intrinsics', nargout=1):
            eng.workspace['fisheye_intrinsics'] = content['fisheye_intrinsics']
        else:
            eng.workspace['fisheye_intrinsics'] = content
    else:
        eng.workspace['fisheye_intrinsics'] = intrinsics

    MappingCoefficients = eng.eval('fisheye_intrinsics.MappingCoefficients', nargout=1)
    ImageSize = eng.eval('fisheye_intrinsics.ImageSize', nargout=1)
    DistortionCenter = eng.eval('fisheye_intrinsics.DistortionCenter', nargout=1)
    StretchMatrix = eng.eval('fisheye_intrinsics.StretchMatrix', nargout=1)

    MappingCoefficients = np.array(MappingCoefficients)[0]
    ImageSize = np.array(ImageSize)[0]
    DistortionCenter = np.array(DistortionCenter)[0]
    StretchMatrix = np.array(StretchMatrix)

    pol = [MappingCoefficients[0], 0, MappingCoefficients[1], MappingCoefficients[2], MappingCoefficients[3]]

    width = int(ImageSize[1])
    height = int(ImageSize[0])
    xc = DistortionCenter[0]
    yc = DistortionCenter[1]

    camera_params = {
        'pol': pol,
        'width': width,
        'height': height,
        'xc': xc,
        'yc': yc,
        'c': StretchMatrix[0, 0],
        'd': StretchMatrix[0, 1],
        'e': StretchMatrix[1, 0],
        'shift_cx': xc - width / 2,
        'shift_cy': yc - height / 2,
    }

    camera_params = to_ocam_model(camera_params)

    return camera_params


def load_matlab_intrinsics(intrinsics):
    if isinstance(intrinsics, str):
        content = eng.load(intrinsics, nargout=1)
        
        if eng.isfield(content, 'fisheye_intrinsics', nargout=1):
            eng.workspace['fisheye_intrinsics'] = content['fisheye_intrinsics']
        else:
            eng.workspace['fisheye_intrinsics'] = content

        return eng.workspace['fisheye_intrinsics']

    raise TypeError("Give path to intrinsics.mat file")


def project_fisheye_points(object_points, intrinsics_mat, tform=eng.rigidtform3d()):
    worldPoints = object_points[:, 0, :]
    worldPoints = matlab.double(np.ascontiguousarray(worldPoints).astype(dtype=np.double))
    projectedPoints = eng.world2img(worldPoints, tform, intrinsics_mat);    
    projectedPoints = np.array(projectedPoints._data).reshape(projectedPoints.size, order='F').astype(dtype=np.float32)

    return projectedPoints[:, None, :]



def convert_intrinsics_to_matlab_cli():
    parser = argparse.ArgumentParser(description='Convert fisheye intrinsics.JSON to matlab format')

    # Add command-line arguments for input parameters
    parser.add_argument('intrinsics', type=str, help='Path to intrinsics.JSON')
    parser.add_argument('--output', type=str, default=None, help='Path to .mat save file')

    args = parser.parse_args()
    
    if args.output is None:
        args.output = args.intrinsics.replace('.json', '.mat')    

    output_path = args.output

    with open(args.intrinsics, 'r') as f:
        intrinsics = json.load(f)

    intrinsics = convert_intrinsics_to_matlab(intrinsics)
    eng.workspace['fisheye_intrinsics'] = intrinsics
    eng.save(output_path, 'fisheye_intrinsics', nargout=0)

    print('Saved to', output_path)


def convert_matlab_to_intrincis_cli():
    parser = argparse.ArgumentParser(description='Convert fisheye matlab format to intrinsics.JSON')

    # Add command-line arguments for input parameters
    parser.add_argument('intrinsics', type=str, help='Path to intrinsics.mat')
    parser.add_argument('--output', type=str, default=None, help='Path to .JSON save file')

    args = parser.parse_args()
    
    if args.output is None:
        args.output = args.intrinsics.replace('.mat', '.json')

    output_path = args.output

    intrinsics = convert_matlab_to_intrincis(args.intrinsics)
    to_ocam_model(intrinsics)   

    with open(output_path, 'w') as f:
        json.dump(intrinsics, f, indent=4)

    print('Saved to', output_path)
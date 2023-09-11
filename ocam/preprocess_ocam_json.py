import json
import numpy as np

from findinvpoly import findinvpoly


def to_ocam_model(path):
    if isinstance(path, str):
        with open(path, 'r') as f:
            cam_model = json.load(f)
    else:
        cam_model = path
            
    json_changed = False
    
    if 'xc' not in cam_model or 'yc' not in cam_model:
        cam_model['xc'] = cam_model['width'] / 2.0 + cam_model['shift_cx']
        cam_model['yc'] = cam_model['height'] / 2.0 + cam_model['shift_cy']
        json_changed = True

    if 'invpol' not in cam_model:
        cx = cam_model['xc']
        cy = cam_model['yc']

        radius = np.sqrt(cx**2 + cy**2)

        cam_model['invpol'] = findinvpoly(cam_model['pol'], radius).tolist()
        json_changed = True


    if json_changed and isinstance(path, str):
        with open(path, 'w') as f:
            json.dump(cam_model, f, indent=4)

    return cam_model

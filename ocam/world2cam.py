import numpy as np


def world2cam(point3D, o):
    o['length_invpol'] = len(o['invpol'])

    point2D = []

    norm = np.linalg.norm(point3D[:2])

    if norm != 0:
        theta = np.arctan(point3D[2] / norm)
        invnorm = 1.0 / norm
        t = theta
        rho = o['invpol'][0]
        t_i = 1.0

        for i in range(1, o['length_invpol']):
            t_i *= t
            rho += t_i * o['invpol'][i]

        x = point3D[0] * invnorm * rho
        y = point3D[1] * invnorm * rho

        point2D.append(x * o['c'] + y * o['d'] + o['xc'])
        point2D.append(x * o['e'] + y + o['yc'])
    else:
        point2D.append(o['xc'])
        point2D.append(o['yc'])

    return point2D


def world2cam_np(point3D, o):
    assert len(point3D.shape) == 3, 'point3D should be a 3D array'
    assert point3D.shape[1] == 1, 'point3D should be a Nx1x3 array'

    point3D = point3D[:, 0, :]

    o['length_invpol'] = len(o['invpol'])

    norm = np.linalg.norm(point3D[:, :2], axis=1)

    points2D = np.zeros((point3D.shape[0], 2), dtype=np.float32)
    points2D[:, 0] = o['xc']
    points2D[:, 1] = o['yc']

    valid_indices = (norm != 0)

    theta = np.arctan(point3D[valid_indices, 2] / norm[valid_indices])
    invnorm = 1.0 / norm[valid_indices]
    t = theta
    rho = np.ones_like(t) * o['invpol'][0]
    t_i = np.ones_like(t) * 1.0

    for i in range(1, o['length_invpol']):
        t_i *= t
        rho += t_i * o['invpol'][i]
    
    x = point3D[valid_indices, 0] * invnorm * rho
    y = point3D[valid_indices, 1] * invnorm * rho
    
    points2D[valid_indices, 0] = x * o['c'] + y * o['d'] + o['xc']
    points2D[valid_indices, 1] = x * o['e'] + y + o['yc']

    return points2D[:, None, :]


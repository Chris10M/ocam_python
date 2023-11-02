import numpy as np

def camera2world_np(point: np.ndarray, depth: np.ndarray, o: dict):
    """
    point: np.ndarray of 2D points on image (n, 1, 2)
    depth: np.ndarray of depth of every 2D points (n)
    """
    assert len(point.shape) == 3, 'point should be a 3D array, Nx1x2'
    assert point.shape[1] == 1 and point.shape[2] == 2, 'point should be a Nx1x2 array'
    
    point = point[:, 0, :]

    img_center = np.array([o['xc'], o['yc']])[None, ...]
    fisheye_polynomial = np.array(o['pol'])

    depth = depth.astype(np.float32)
    point_centered = point.astype(np.float32) - img_center
    x = point_centered[:, 0]
    y = point_centered[:, 1]
    distance_from_center = np.sqrt(np.square(x) + np.square(y))
    
    z = np.polyval(p=fisheye_polynomial[::-1], x=distance_from_center)
    point_3d = np.array([x, y, z])  # 3, n
    norm = np.linalg.norm(point_3d, axis=0)
    point_3d = point_3d / norm * depth
    point_3d = point_3d.transpose()

    point_3d = point_3d[:, None, ...]
    return point_3d

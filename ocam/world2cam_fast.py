import numpy as np

def world2cam_fast(M, ocam_model):
    M = M.T

    assert len(M.shape) == 2, 'M must be a N x 3 Points'
    
    # ss = ocam_model['ss']
    xc = ocam_model['xc']
    yc = ocam_model['yc']
    width = ocam_model['width']
    height = ocam_model['height']
    c = ocam_model['c']
    d = ocam_model['d']
    e = ocam_model['e']
    pol = ocam_model['pol']
    
    npoints = M.shape[1]
    theta = np.zeros(npoints)
    
    NORM = np.sqrt(M[0, :] ** 2 + M[1, :] ** 2)
    
    ind0 = np.where(NORM == 0)[0]  # Indices of points along the z-axis
    NORM[ind0] = np.finfo(float).eps  # To avoid division by zero later
    
    theta = np.arctan(M[2, :] / NORM)
    
    rho = np.polyval(pol, theta)  # Distance in pixels of reprojected points from the image center
    
    x = M[0, :] / NORM * rho
    y = M[1, :] / NORM * rho
    

    # Add center coordinates
    m = np.zeros((2, npoints))
    m[0, :] = x * c + y * d + xc
    m[1, :] = x * e + y + yc
    
    return m.T
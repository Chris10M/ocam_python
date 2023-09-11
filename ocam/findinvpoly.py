import numpy as np


def findinvpoly(ss, radius):
    maxerr = np.inf
    N = 1
    while maxerr > 0.01:
        N += 1
        pol, err, N = findinvpoly2(ss, radius, N)
        maxerr = np.max(err)
    
    return np.flip(pol)

def findinvpoly2(ss, radius, N):
    theta = np.arange(-np.pi/2, 1.20, 0.01)

    r = invFUN(ss, theta, radius)
    ind = np.where(r != np.inf)
    theta = theta[ind]
    r = r[ind]

    pol = np.polyfit(theta, r, N)
    err = np.abs(r - np.polyval(pol, theta))
    
    return pol, err, N


def invFUN(ss, theta, radius):
    m = np.tan(theta)
    r = []

    poly_coef = np.flip(ss)
    poly_coef_tmp = np.copy(poly_coef)

    for j in range(len(m)):
        poly_coef_tmp[-2] = poly_coef[-2] - m[j]
        rhoTmp = np.roots(poly_coef_tmp)
        
        
        res = rhoTmp[(np.imag(rhoTmp) == 0) & (rhoTmp > 0) & (rhoTmp < radius)]
        res = res.real
        
        if len(res) == 0 or len(res) > 1:
            r.append(np.inf)
        else:
            r.append(res[0])

    r = np.array(r).astype(np.float32)  
    return r

import numpy as np
import cv2

def error_handle(orig_img, offsets, method, radius):
    """
    Handles some errors.
    """
    if orig_img.ndim != 2 and orig_img.ndim != 3:
        raise TypeError("Incorrect number of dimensions (excepted 2 or 3)")

    if not isinstance(radius, int):
        raise TypeError('`radius` must be int')

    if radius < 1:
        raise ValueError('`radius` must be greater or equal 1')

    if method not in ('mean', 'gaussian'):
        raise NotImplementedError('unsupported method %s' % method)

    if max(offsets) > 3 or min(offsets) < 0:
        raise ValueError('`offsets` must be 0, 1, 2, 3')

def indicies(stddevs, offsets):
    """
    Returns a new list of indices with some offsets
    """
    sorted_dev = np.argsort(stddevs, axis = 0)
    indices = sorted_dev[0]
    _, w, h = stddevs.shape
    o = 0
    for i in range(w):
        for j in range(h):
            if o >= len(offsets):
                break
            indices[i][j] = sorted_dev[offsets[o]][i][j]
        if o >= len(offsets):
            break
    return indices

def kuwahara(orig_img, offsets = [0], method='mean', radius=3, sigma=None, grayconv=cv2.COLOR_BGR2GRAY, image_2d=None):
    # fork of https://github.com/yoch/pykuwahara
    # no anisotropic methods
    # todos: refactor the code so it looks nicer to me
    # todos: implement anisotropic window

    error_handle(orig_img, offsets, method, radius)

    if method == 'gaussian' and sigma is None:
        sigma = -1

    image = orig_img.astype(np.float32, copy=False)

    if image_2d is not None:
        image_2d = image_2d.astype(image.dtype, copy=False)

    avgs = np.empty((4, *image.shape), dtype=image.dtype)
    stddevs = np.empty((4, *image.shape[:2]), dtype=image.dtype)

    if image.ndim == 3:
        if image_2d is None:
            image_2d = cv2.cvtColor(orig_img, grayconv).astype(image.dtype, copy=False)
        avgs_2d = np.empty((4, *image.shape[:2]), dtype=image.dtype)
    elif image.ndim == 2:
        image_2d = image
        avgs_2d = avgs

    squared_img = image_2d ** 2

    if method == 'mean':
        kxy = np.ones(radius + 1, dtype=image.dtype) / (radius + 1)    # kernelX and kernelY (same)
    elif method == 'gaussian':
        kxy = cv2.getGaussianKernel(2 * radius + 1, sigma, ktype=cv2.CV_32F)
        kxy /= kxy[radius:].sum()   # normalize the semi-kernels
        klr = np.array([kxy[:radius+1], kxy[radius:]])
        kindexes = [[1, 1], [1, 0], [0, 1], [0, 0]]

    # the pixel position for all kernel quadrants
    shift = [(0, 0), (0,  radius), (radius, 0), (radius, radius)]

    # Calculation of averages and variances on subwindows
    for k in range(4):
        if method == 'mean':
            kx = ky = kxy
        elif method == 'gaussian':
            kx, ky = klr[kindexes[k]]
        cv2.sepFilter2D(image, -1, kx, ky, avgs[k], shift[k])
        if image.ndim == 3: # else, this is already done...
            cv2.sepFilter2D(image_2d, -1, kx, ky, avgs_2d[k], shift[k])
        cv2.sepFilter2D(squared_img, -1, kx, ky, stddevs[k], shift[k])
        stddevs[k] = stddevs[k] - avgs_2d[k] ** 2    # compute the final variance on subwindow

    # NOTE HERE IS THE IMPORTANT OFFSET ADDITION
    indices = indicies(stddevs, offsets)

    # Building the filtered image
    if image.ndim == 2:
        filtered = np.take_along_axis(avgs, indices[None,...], 0).reshape(image.shape)
    else:   # then avgs.ndim == 4
        filtered = np.take_along_axis(avgs, indices[None,...,None], 0).reshape(image.shape)

    return filtered.astype(orig_img.dtype)
import numpy as np
from random import shuffle

def combine(img1, img2, method='rand'):
    """
    Want to make it 1 image == 1 message
    Save the original image
    """
    if img1.shape != img2.shape:
        raise TypeError('incorrect number of dimensions')
    if method not in ['avg', 'rand', 'vert', 'hori']:
        raise TypeError('`method` is not one of the combination methods')
    w, h, c = img1.shape
    new_image = np.empty((2*w, 2*h, c), dtype=img1.dtype)
    for i in range(w):
        for j in range(h):
            c1, c2 = img1[i][j], img2[i][j]
            new_image[2*i][2*j] = c1
            new_image[2*i+1][2*j+1] = c2

            if method == 'avg':
                c3 = c4 = (c1 + c2)/2
            elif method == "vert":
                c3 = c1
                c4 = c2
            elif method == "hori":
                c3 = c2
                c4 = c1
            elif method == "rand": # minimize streaking artifacts
                li = [c1, c2, c1, c2]
                shuffle(li)
                c3, c4 = li[:2]

            new_image[2*i+1][2*j] = c3
            new_image[2*i][2*j+1] = c4
    return new_image
import numpy as np
import cv2 as cv
from ast import literal_eval

def kmeans(path, k = 8):
    img = cv.imread(path)
    z = img.reshape((-1,3))

    # convert to np.float32
    z = np.float32(z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret,label,center=cv.kmeans(z,k,None,criteria,10,cv.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    return res.reshape((img.shape))

def to_hash(list, joiner = ','):
      
    # Converting integer list to string list
    s = [str(i) for i in list]
      
    # Join list items using join()
    return joiner.join(s)

def from_hash(str, joiner = ','):
      
    b, g, r = str.split(sep=joiner)
    return (int(b),int(g),int(r))

def get_pallet(path, k = 3, debug = False):
    img = kmeans(path, k)
    h = img.shape[0]
    w = img.shape[1]
    a = w*h

    pallet = []
    d = dict()

    for y in range(w):
        for x in range(h):
            c = to_hash(img[x,y][:3])
            if c in d:
                d[c]+= 1
            else:
                d[c]= 1

    for (k, v) in sorted(d.items(), key=lambda x: x[1], reverse=True):
        pallet.append((from_hash(k), round(v/a,4)))
   
    return pallet


pallet = get_pallet('images/pallet.jpg',16, True)

print(pallet)

cv.waitKey(0)
cv.destroyAllWindows()
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label


def neighbours4(y, x):
    return (y, x+1), (y, x-1), (y-1, x), (y+1, x)

def neighbours8(y, x):
     return neighbours4(y, x) + ((y-1, x+1), (y+1, x+1), (y-1, x-1), (y+1, x-1))

def get_boundaries(labeled, label=1, connectivity=neighbours4):
    pos = np.where(labeled == label)
    bounds = []
    for y, x in zip(*pos):
        for yn, xn in connectivity(y, x):
            if yn < 0 or yn > labeled.shape[0]-1:
                bounds.append((y, x))
                break
            elif xn < 0 or xn > labeled.shape[1]-1: 
                bounds.append((y, x))
                break
            elif labeled[yn, xn] == 0:
                bounds.append((y, x))
                break
    return bounds

def sorting(bds):
    bounds = bds
    y0, x0 = bounds[0]
    y, x = bounds[1]
    sorted = []
    while (y!=y0 or x !=x0):
        bounds.pop(bounds.index((y, x)))  
        if (y, x+1) in bounds:
            sorted.append((y, x+1))
            x+=1
        elif (y+1,x+1) in bounds:
            sorted.append((y+1,x+1))
            y+=1
            x+=1
        elif (y+1,x) in bounds:
            sorted.append((y+1,x))
            y+=1
        elif (y+1,x-1) in bounds:
            sorted.append((y+1,x-1))
            y+=1
            x-=1
        elif (y,x-1) in bounds:
            sorted.append((y,x-1))
            x-=1
        elif (y-1,x-1) in bounds:
            sorted.append((y-1,x-1))
            y-=1
            x-=1
        elif (y-1,x) in bounds:
            sorted.append((y-1,x))
            y-=1
        elif (y-1,x+1) in bounds:
            sorted.append((y-1,x+1))
            y-=1
            x+=1
    return sorted
def point(p1, p2):
    y1, x1  = p1
    y2, x2  = p2
    y = y2-y1
    x = x2-x1
    if y == 0 and x==1:
        return 0
    elif y==1 and x==1:
        return 1
    elif y==1 and x==0:
        return 2
    elif y==1 and x==-1:
        return 3
    elif y==0 and x==-1:
        return 4
    elif y==-1 and x==-1:
        return 5
    elif y==-1 and x==0:
        return 6
    elif y==-1 and x==1:
        return 7

def chain(bounds):
    d = []
    for i in range(1, len(bounds)-1):
        d.append(point(bounds[i], bounds[i+1]))
    return d
        

img = np.load("similar.npy")
# img = np.zeros((10, 10))
# img[2:5, 2:5]=1
labeled = label(img)
for i in range(1, np.max(labeled)):
    sorted = sorting(get_boundaries(labeled, i))
    print(get_boundaries(labeled, i))
    print(f'Фигура: {i}, последовательность {chain(sorted)}')
plt.imshow(labeled)
plt.show()

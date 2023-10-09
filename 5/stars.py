import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import binary_dilation, binary_erosion, binary_opening, binary_closing

def check(B, y, x):
    # if not 0 <= y < B.shape[0]:
    #     return False
    # if not 0 <= x < B.shape[1]:
    #     return False
    # if B[y, x] != 0:
    #     return True
    # return False
    return x>=0 and y>=1 and B[y, x]

def neighbours2(B, y, x):
    left = y, x-1
    top = y-1, x
    if not check(B, *left):
        left = None
    if not check(B, *top):
        top = None
    return left, top

def find(label, linked):
    j = label
    while linked[j] != 0:
        j = linked[j]
    return j

def union(label1, label2, linked):
    j = find(label1, linked)
    k = find(label2, linked)
    if j != k:
        linked[k] = j

def two_pass_labeling(B):
    linked = np.zeros(B.size//2, dtype="uint16")
    labeled = np.zeros_like(B, dtype="uint16")
    label = 1
    for row in range(B.shape[0]):
        for col in range(B.shape[1]):
            if B[row][col] != 0:
                lbs = []
                nbs = list(filter(None, neighbours2(B, row, col)))
                for nb in nbs:
                    lbs.append(labeled[nb])
                if not lbs:
                    label += 1
                    m = label
                else:
                    m = min(lbs)
                labeled[row][col] = m
                for nb in nbs:
                    lb  = labeled[nb]
                    if lb != m:
                        union(m, lb, linked)
    
    for row in range(B.shape[0]):
        for col in range(B.shape[1]):
            if B[row, col] != 0:
                new_label = find(labeled[row, col], linked)
                # print(new_label)
                if new_label != labeled[row, col]:
                    labeled[row, col] = new_label
    arr = []
    for row in range(labeled.shape[0]):
        for col in range(labeled.shape[1]):
            if labeled[row, col] != 0:
                if labeled[row, col] not in arr:
                    arr.append(labeled[row, col])
                labeled[row, col] = arr.index(labeled[row, col]) + 1
    # print(labeled)
    return labeled

img = np.load("stars.npy")
# plt.imshow(img)
# plt.show()
# struct1 = [[1, 1, 1],
#           [1, 1, 1],
#           [1, 1, 1]]

struct2 = [[1, 0, 0, 0, 1], [0, 1, 0, 1, 0], [0, 0, 1, 0, 0], [0, 1, 0, 1, 0], [1, 0, 0, 0, 1]]
struct3 = [[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [1, 1, 1, 1, 1], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0]]
for struct in (struct2, struct3):
    image = binary_erosion(img, struct)
    image = two_pass_labeling(image)
    print(np.max(image))

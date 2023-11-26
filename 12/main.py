import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
import math

def get_centroid(labeled, label=1):
  pos = np.where(labeled == label)
  return (int)(pos[0].mean()), (int)(pos[1].mean())

def add_to_circle(pos, circ):
    xl, yl = get_centroid(labeled, pos)
    circ[0].append(xl)
    circ[1].append(yl)

circ1 = [[], []]
circ2 = [[], []]
circ3 = [[], []]
circles = [circ1, circ2, circ3]

image = np.load(f"/content/out/h_0.npy")
labeled = label(image)
for i, circ in enumerate(circles, start=1):
  add_to_circle(i, circ)

for i in range(1, 100):
    image = np.load(f"/content/out/h_{i}.npy")
    labeled = label(image)
    for lbl in range(1, 4):
        pos = np.where(labeled == lbl)
        for x, y in zip(*pos):
            for circ in circles:
                if circ[0] and circ[0][-1] == x and circ[1] and circ[1][-1] == y:
                    add_to_circle(lbl, circ)

for circ in circles:
    plt.plot(circ[0], circ[1])
plt.show()

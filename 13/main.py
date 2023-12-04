import matplotlib.pyplot as plt
import cv2
import numpy as np
from skimage.measure import label, regionprops

image = plt.imread("balls_and_rects.png")
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
binary = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) > 0

labeled = label(binary)
h = hsv[:, :, 0]
regions = regionprops(labeled)
colors = []
circles = []
rectangles = []

for region in regions:
    pixels = h[region.coords]
    r = h[region.bbox[0]:region.bbox[2], region.bbox[1]:region.bbox[3]]
    colors.extend(np.unique(r)[1:])
    if np.min(r) == 0.0:
        circles.append(r)
    else:
        rectangles.append(r)

clusters = []
while colors:
    color1 = colors.pop(0)
    clusters.append([color1])
    for color2 in colors.copy():
        if abs(color1 - color2) < 5:
            clusters[-1].append(color2)
            colors.pop(colors.index(color2))

shades = {}
for cluster in clusters:
    shades[int(np.mean(cluster))] = [int(np.min(cluster)) - 1, int(np.max(cluster) + 1)]

print(f"Фигуры: {np.max(labeled)}")
print(f"Прямоугольники: {len(rectangles)}")
print(f"Круги: {len(circles)}")
print("shade (color) | rectangles(count) | circles(count)")
for shade in sorted(shades.keys()):
    sum_rect = sum(1 for rect in rectangles if shades[shade][0] < np.max(rect) < shades[shade][1])
    sum_circ = sum(1 for circ in circles if shades[shade][0] < np.max(circ) < shades[shade][1])
    
    print(f"{shade}                   {sum_rect}                    {sum_circ}")

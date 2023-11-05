import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

def filling_factor(region):
    return region.image.mean()

def recognize(region):
    if filling_factor(region) == 1:
        return "-"
    else:
        euler = region.euler_number
        if euler == -1:#B or 8
             if 1 in region.image.mean(0)[:2]:
                 return "B"
             else:
                 return "8"
        elif euler == 0:# A 0 P D 
            tmp = region.image.copy()
            if 1 in region.image.mean(0)[:2]:
                tmp[len(tmp[:, 0])//2, :] = 1
                tmp_labeled = label(tmp)
                tmp_regions = regionprops(tmp_labeled)
                if tmp_regions[0].euler_number == -1:
                    return "D"
                elif tmp_regions[0].euler_number == 0:
                    return "P"
            tmp[-1, :] = 1
            tmp_labeled = label(tmp)
            tmp_regions = regionprops(tmp_labeled)
            if 1 in region.image.mean(0) and region.eccentricity < 0.5:
                return '*'
            if tmp_regions[0].euler_number == -1:
                return "A"
            return "0"
        else: # 1 W X * /
            if 1 in region.image.mean(0):   
                return "1"
            tmp = region.image.copy()
            tmp[[0, -1], :] = 1
            tmp_labeled = label(tmp)
            tmp_regions = regionprops(tmp_labeled)
            euler = tmp_regions[0].euler_number 
            if euler == -1:
                return "X"
            elif euler == -2:
                return "W"
            if region.eccentricity > 0.5:
                return "/"
            else:
                return "*"  
    return "?"

img = plt.imread('symbols.png')
binary = img.mean(2)
binary[binary!=0] = 1

labeled = label(binary)
print(np.max(labeled))

regions = regionprops(labeled)

counts = {}

for region in regions:
    symbol = recognize(region)
    if symbol not in counts:
        counts[symbol] = 0
    counts[symbol] += 1

print(counts) 
# print((labeled.max())/labeled.max())
print(f'{(labeled.max()-counts.get("?", 0))/labeled.max()}')
# plt.imshow(img)
# plt.imshow(regions[4].image)
# plt.imshow(regions[7].euler_number)
plt.show()

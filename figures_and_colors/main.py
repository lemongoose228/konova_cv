import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv
import numpy as np

im = plt.imread("balls_and_rects.png")

binary = im.mean(2)
binary[binary>0] = 1
labeled = label(binary)
regions = regionprops(labeled)

print("Всего фигур:", np.max(labeled))

im_hsv = rgb2hsv(im)

colors = []

for region in regions:
    cy, cx = region.centroid
    color = im_hsv[int(cy), int(cx)][0]
    colors.append((round(float(color), 2), region))

circles = {}
rectangles = {}

for elem in colors:
    flag = True
    if elem[1].area == elem[1].area_bbox:
        for key in rectangles.keys():
            if key - 0.05 < elem[0] < key + 0.05:
                rectangles[key] += 1
                flag = False
                break

        if flag:
            rectangles[elem[0]] = 1
    else:
        for key in circles.keys():
            if key - 0.05 < elem[0] < key + 0.05:
                circles[key] += 1
                flag = False
                break

        if flag:
            circles[elem[0]] = 1

    flag = True

print("\nКруги:")
for i in circles:
    print(f"Оттенок {i}:", circles[i])

print("\nПрямоугольники:")
for i in rectangles:
    print(f"Оттенок {i}:", rectangles[i])

# rounded_colors = np.round(colors, 1)
# unique_colors = np.unique(rounded_colors)
# print(len(unique_colors))

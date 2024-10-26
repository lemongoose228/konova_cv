import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label


def area(LB, label=1):
    return np.sum(LB == label)


image = label(np.load("coins.npy"))

nominals = [1, 2, 5, 10]
counts = dict()

for i in range(1, image.max() + 1):
    ar = area(image, i)
    if ar not in counts:
        counts[ar] = 0
    counts[ar] += 1
print(counts)

total = 0

for i, k in enumerate(sorted(counts)):
    total += counts[k] * nominals[i]


print(total)
plt.imshow(image)
plt.show()

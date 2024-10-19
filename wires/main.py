import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import binary_closing
from scipy.ndimage import binary_erosion
from scipy.ndimage import binary_dilation
from scipy.ndimage import binary_opening
from scipy.datasets import face


def neighbours2(y, x):
    return (y, x - 1), (y - 1, x)


def exist(B, nbs):
    left, top = nbs
    if (left[0] >= 0 and left[0] < B.shape[1] and
            left[1] >= 0 and left[1] < B.shape[0]):
        if B[left] == 0:
            left = None
    else:
        left = None

    if (top[0] >= 0 and top[0] < B.shape[1] and
            top[1] >= 0 and top[1] < B.shape[0]):
        if B[top] == 0:
            top = None
    else:
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


def two_pass(B):
    LB = np.zeros_like(B)
    linked = np.zeros(B.size // 2 + 1, dtype="uint")
    label = 1

    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if B[y, x] != 0:
                nbs = neighbours2(y, x)
                existed = exist(B, nbs)
                if existed[0] is None and existed[1] is None:
                    m = label
                    label += 1
                else:
                    lbs = [LB[n] for n in existed if n is not None]
                    m = min(lbs)

                LB[y, x] = m

                for n in existed:
                    if n is not None:
                        lb = LB[n]
                        if lb != m:
                            union(m, lb, linked)

    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if B[y, x] != 0:
                new_label = find(LB[y, x], linked)
                if new_label != LB[y, x]:
                    LB[y, x] = new_label

    unique_val = np.unique(LB)

    new_label = 1

    for old_val in unique_val:
        if old_val != 0:
            LB[LB == old_val] = new_label
            new_label += 1

    return LB

def count_figures(image):
    return np.unique(image[image != 0])

def cut_figures(B):
    a = count_figures(B)
    struct = np.ones((3, 1))
    result = []
    for i in a:
        wire = B == i
        whire_er = binary_erosion(wire, struct)
        result.append(whire_er)
    return result


image1 = np.load("wires1npy").astype("uint8")
image2 = np.load("wires2npy").astype("uint8")
image3 = np.load("wires3npy").astype("uint8")
image4 = np.load("wires4npy").astype("uint8")
image5 = np.load("wires5npy").astype("uint8")
image6 = np.load("wires6npy").astype("uint8")


wire_cuted = cut_figures(two_pass(image5))

for i, wire in enumerate(wire_cuted):
    parts = len(count_figures(two_pass(wire.astype(int))))
    if parts != 1 and parts != 0:
        print("Провод ", i + 1, " порван на ", parts, "части")
    elif parts == 0:
        print("Провод ", i + 1, " порван полностью")
    else:
        print("Провод ", i + 1, " цел")
    plt.figure()
    plt.imshow(wire)
plt.show()

import numpy as np
import matplotlib.pyplot as plt
# from scipy.ndimage import binary_closing
from scipy.ndimage import binary_erosion
# from scipy.ndimage import binary_dilation
# from scipy.ndimage import binary_opening

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



def find_crosses(B):
    struct = np.array([[1, 0, 0, 0, 1],
                       [0, 1, 0, 1, 0],
                       [0, 0, 1, 0, 0],
                       [0, 1, 0, 1, 0],
                       [1, 0, 0, 0, 1], ])
    B_er = binary_erosion(B, struct)
    return B_er

    pass
def find_plusses(B):
    struct = np.array([[0, 0, 1, 0, 0],
                       [0, 0, 1, 0, 0],
                       [1, 1, 1, 1, 1],
                       [0, 0, 1, 0, 0],
                       [0, 0, 1, 0, 0],])
    B_er = binary_erosion(B, struct)
    return B_er



image = np.load("stars.npy").astype("int")

plusses = find_plusses(two_pass(image))
crosses = find_crosses(two_pass(image))

result = plusses + crosses

counter = 0

for i in range(result.shape[0]):
    for j in range(result.shape[1]):
        if result[i][j]:
            counter += 1


print(counter)

plt.imshow(image)
plt.show()

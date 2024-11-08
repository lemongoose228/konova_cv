import numpy as np
from skimage.measure import label
import matplotlib.pyplot as plt

def count_figures(B):
    num_figures = np.unique(label(B)).max()
    return num_figures

image = np.load("ps.npy").astype("uint8")

res = count_figures(image)
print("Всего фигур:", res)
plt.imshow(image)
plt.show()

import matplotlib.pyplot as plt
import numpy as np

def show_fun(img):
    plt.figure()
    plt.imshow(np.rot90(img))
    plt.show()
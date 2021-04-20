from PIL import Image
from slice import slice
import matplotlib.pyplot as plt
import numpy as np
import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

def outline(gray_array):
    rows, cols = gray_array.shape
    mag = np.zeros([rows, cols], np.float)
    for x in range(1, rows - 1):
        for y in range(1, cols - 1):
            gx = 0.5 * gray_array[x + 1, y] - 0.5 * gray_array[x - 1, y]
            gy = 0.5 * gray_array[x, y + 1] - 0.5 * gray_array[x, y - 1]
            mag[x, y] = np.power(gx * gx + gy * gy, 0.5)
    return mag

def histogram_balanced(image_array):
    row,col=image_array.shape
    hist, bins = np.histogram(image_array.flatten(), row*col,[0,image_array.max()])
    cdf = hist.cumsum()
    cdf_tmp = np.ma.masked_equal(cdf, 0)  # 除去直方图中的0值
    cdf_tmp = np.divide(np.multiply((cdf_tmp - cdf_tmp.min()),255), image_array.size)
    cdf2 = np.ma.filled(cdf_tmp, 0)
    return cdf2[image_array]

def threshold(img,th,choice="TOZERO"):
    #img = histogram_balanced(img)
    if choice=='BINARY':
        ret, thresh = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)
    if choice == 'BINARY_INV':
        ret, thresh = cv2.threshold(img, th, 255, cv2.THRESH_BINARY_INV)
    if choice == 'TRUNC':
        ret, thresh = cv2.threshold(img, th, 255, cv2.THRESH_TRUNC)
    if choice == 'TOZERO':
        ret, thresh = cv2.threshold(img, th, 255, cv2.THRESH_TOZERO)
    if choice == 'TOZERO_INV':
        ret, thresh = cv2.threshold(img, th, 255, cv2.THRESH_TOZERO_INV)
    return thresh

# path='C:/Users/zhangke/Desktop/software/BRATS_HG0015_T1C.mha'
# data=slice.read_img(path)
# img=threshold(data[:,80,:])
# plt.set_cmap("gray")
# #plt.imshow(data[:,80,:])
# plt.imshow(img)
# plt.show()
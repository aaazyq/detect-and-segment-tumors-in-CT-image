from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import matplotlib.pyplot as plt
import slice
from pylab import *
from skimage import transform,data

class adjust():
    def contrast(array, alpha):
        newarray = array
        m = array.max()
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                if (array[i][j] < m / 4):
                    newarray[i][j] = alpha * array[i][j]
                elif (array[i][j] > m * 3 / 4):
                    newarray[i][j] = alpha * array[i][j] + (1 - alpha) * m
                else:
                    newarray[i][j] = (2 - alpha) * array[i][j] + (alpha - 1) * m / 2
        return newarray

    def bright(array, brightness):
        gamma = 1 / brightness
        max_num = array.max()
        if max_num > 0:
            newarray = max_num * (array / max_num) ** gamma
        else:
            newarray = max_num * (array) ** gamma
        return newarray

    def resize(array, alpha):
        newarray = transform.rescale(array, alpha)
        return newarray

    def enlarge(x,y, array, alpha):
        newarray = adjust.resize(array, alpha)  # 放大后的矩阵
        returnarray = newarray[int((alpha - 1) * y):int((alpha - 1) * y) + array.shape[0],
                      int((alpha - 1) * x):int((alpha - 1) * x) + array.shape[1]]
        return returnarray

# path = "C:/Users/zhangke/Desktop/braintumor/BRATS_HG0015_FLAIR.mha"
# a = slice.slice.return_S_array(path,S=20)
# plt.set_cmap("gray")
# plt.imshow(adjust.enlarge(100,111,a,2))
# plt.show()

# #img=contrast(image,1)
# img = image.convert('L')
# plt.set_cmap("gray")
# plt.imshow(gray(a,0.5))
# print(a[150])
# #plt.imshow(image.convert('L'))
# plt.show()
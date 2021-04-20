# encoding=utf8
import SimpleITK as sitk
from skimage import io,transform
import matplotlib.pyplot as plt
import numpy as np
class slice():
    def read_img(path):
        img = sitk.ReadImage(path)
        data = sitk.GetArrayFromImage(img)
        data = data - np.mean(data)
        data = np.divide(data, data.max())
        data = np.multiply(data, 255)
        return data
    def show_A(path,A):
        # 显示A面
        data = slice.read_img(path)
        img = data[:, A, :]
        img = transform.rotate(img, -90, resize=True)
        # io.imshow(img, cmap='gray')
        plt.set_cmap("gray")
        plt.imshow(img)
        plt.axis('off')
        plt.show()
    def show_C(path, C):
        # 显示C面
        data = slice.read_img(path)
        img = data[:, :, C]
        img = transform.rotate(img, -90, resize=True)
        io.imshow(img, cmap='gray')
        io.show()
    def show_S(path, S):
        # 显示S面
        data = slice.read_img(path)
        io.imshow(data[S, :, :], cmap='gray', )
        io.show()
    def return_A_array(path, A):
        # 返回A面的array数据
        data = slice.read_img(path)
        img = data[:, A, :]
        img = transform.rotate(img, -90, resize=True)
        return img
    def return_C_array(path, C):
        # 返回C面的array数据
        data = slice.read_img(path)
        img = data[:, :, C]
        img = transform.rotate(img, -90, resize=True)
        return img
    def return_S_array(path, S):
        # 返回S面的array数据
        data = slice.read_img(path)
        img = data[S, :, :]
        return img
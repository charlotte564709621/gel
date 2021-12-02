import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from urllib3.connectionpool import xrange

img = cv.imread('image/gel_img1.png')
gray_img =cv.cvtColor(img,cv.COLOR_BGR2GRAY)

px = gray_img.item(50,50)
print(px)
print(gray_img.shape)
print(gray_img.size)
print(gray_img.dtype)
# equ = cv.equalizeHist(gray_img)
# res = np.hstack((gray_img,equ))
# hist = cv.calcHist([res],[0],None,[256],[0,256])
# plt.hist(res.ravel(),256,[0,256])
# plt.show()

img = cv.imread('image/home.png',0)
# 全局阈值
ret1,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
# Otsu阈值
ret2,th2 = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
# 高斯滤波后再采用Otsu阈值
blur = cv.GaussianBlur(img,(5,5),0)
ret3,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
# 绘制所有图像及其直方图
images = [img, 0, th1,
          img, 0, th2,
          blur, 0, th3]
titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
          'Original Noisy Image','Histogram',"Otsu's Thresholding",
          'Gaussian filtered Image','Histogram',"Otsu's Thresholding"]
for i in xrange(3):
    plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
    plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
    plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
    plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
    plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2],'gray')
    plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
plt.show()


while True:
    if ord('q') == cv.waitKey(0):
        break
cv.destroyAllWindows()
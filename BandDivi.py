import cv2 as cv
import numpy as np
from matplotlib import pylab as plt
from UncodeChinese import cvImgAddText
img = cv.imread('image/gel1/lane10.png')
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

#旋转
trans_img = cv.transpose(gray_img)
gray_img = cv.flip(trans_img, 0)
#原图复制保留
origin_gray_img = gray_img.copy()

# 高斯滤波后再采用Otsu阈值
blur = cv.GaussianBlur(gray_img,(5,5),3)
th = cv.adaptiveThreshold(blur,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,0)
# 去噪
th = cv.medianBlur(th,9) # 中值滤波
gauss_img = th
cv.imshow("gauss",gauss_img)
#读取白点数量
row,col = gauss_img.shape
print(row,col)
array = np.zeros(col)
#按列遍历
for l in range(col):
    total = 0
    for r in range(row):
        px = gauss_img.item(r, l)
        if (px == 255):
            total = total+1
    array[l] = total
# 找条带分界点
boundary = []
for l in range(col-1):
        if ((array[l] == 0 and array[l + 1] != 0)or(array[l]!=0 and (array[l+1] == 0))):
            boundary.append(l)
print(boundary)

x=range(0,col)
y=array[x]

plt.subplot(211);plt.plot(x,y)
plt.title('baidian');plt.xlim([0,col])
plt.subplot(212);plt.imshow(origin_gray_img, cmap='gray')
plt.title('origin');plt.xticks([]), plt.yticks([])
plt.show()
#画条带，添加文字，裁剪条带
band_img = origin_gray_img.copy()
print(len(boundary))
for i in range(0,len(boundary),2):
    bandNo = int(i/2+1)#条带序号
    #画条带
    band_img = cv.rectangle(band_img, (boundary[i],0), (boundary[i+1],col), (0, 255, 0), 2)
    band_img = cv.rectangle(band_img, (boundary[0], 0), (boundary[1], col), (0, 255, 0), 2)
    #标记条带
    band_img = cvImgAddText(band_img, str(bandNo), boundary[i]+4, 5, (0,255,0),25)

    cropped = gray_img[0:col, boundary[i]:boundary[i + 1]]
    # 旋转
    cropped = cv.transpose(cropped)
    cropped = cv.flip(cropped, 1)
    cv.imwrite('image/gel1/band'+str(bandNo)+'.png',cropped)
cv.imshow('band_img',band_img)



while True:
    if ord('q') == cv.waitKey(0):
        break
cv.destroyAllWindows()
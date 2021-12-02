import cv2 as cv
import numpy as np
from matplotlib import pylab as plt
from UncodeChinese import cvImgAddText
img = cv.imread('image/DNA.png')

gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# 高斯滤波后再采用Otsu阈值
blur = cv.GaussianBlur(gray_img,(5,5),0)
ret3,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
gauss_img = th3
# cv.imshow('gauss',gauss_img)
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
#画条带，添加文字，裁剪条带
lane_img = gray_img.copy()
print(len(boundary))
for i in range(0,len(boundary)-1,2):
    bandNo = int(i/2+1)#条带序号
    #画条带
    lane_img = cv.rectangle(lane_img, (boundary[i],0), (boundary[i+1],col), (0, 255, 0), 2)
    lane_img = cv.rectangle(lane_img, (boundary[0], 0), (boundary[1], col), (0, 255, 0), 2)
    #标记条带
    lane_img = cvImgAddText(lane_img, '泳道' + str(bandNo), boundary[i]+4, 5, (0,255,0),15)

    cropped = gray_img[0:col, boundary[i]:boundary[i + 1]]
    cv.imwrite('image/gel1/lane'+str(bandNo)+'.png',cropped)
cv.imshow('lane_img',lane_img)

# 绘制光强图谱
for i in range(1,int(len(boundary)/2)):
    img = cv.imread('image/gel1/lane'+str(i)+'.png')
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    row,col = img.shape
    array = np.zeros(row)
    for r in range(row):
     total = 0
     for l in range(col):
         px = img.item(r, l)
         total += px
         array[r] = total
x=range(0,row)
y=array[x]
plt.plot(x,y)
plt.xlim([0,row])
plt.show()


while True:
    if ord('q') == cv.waitKey(0):
        break
cv.destroyAllWindows()
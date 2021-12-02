import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math
img = cv.imread('image/gel1/lane5.png')
gray_img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

row,col = gray_img.shape

array = np.zeros(row)
max_gray_level = 0#最大灰度值
for r in range(row):
    total = 0
    for l in range(col):
        px = gray_img.item(r, l)
        if( px > max_gray_level):
            max_gray_level = px
        total += px
        array[r] = total
print(max_gray_level)

IOD = 0#积分光密度值
for r in range(row):
    for l in range(col):
        px = gray_img.item(r,l)
        OD = math.log(max_gray_level,px)
        IOD += OD
print(IOD)

x=range(0,row)
y=array[x]
plt.plot(x,y)
plt.xlim([0,row])
plt.show()
import cv2 as cv
import numpy as np
from UncodeChinese import cvImgAddText
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont


img = cv.imread('image/gel1/lane1.png')

org_img = img.copy()
#cv.imshow('org_img',org_img)
gray_img =cv.cvtColor(img,cv.COLOR_BGR2GRAY)
#cv.imshow('gray_img',gray_img)

#print(img.item(10,10,2))
img.itemset((10,10,2),100)
#print(img.item(10,10,2))

#print(img.size,img.dtype)

(h, w) = img.shape[:2]
# 这里的第一个参数为旋转中心，第二个为旋转角度，第三个为旋转后的缩放因子
# 可以通过设置旋转中心，缩放因子，以及窗口大小来防止旋转后超出边界的问题
M=cv.getRotationMatrix2D((h/2,w/2),45,0.6)
# 第三个参数是输出图像的尺寸中心
dst=cv.warpAffine(img,M,(h,w))
#cv.imshow('dst',dst)

roc=np.rot90(img)
#cv.imshow('roc',roc)

edges = cv.Canny(img,100,100)
#cv.imshow('edge_img0',edges)



#绘制独立轮廓
ret,thresh = cv.threshold(gray_img,127,255,0)
contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(img, contours, -1, (0,255,0), 3)
edge_img = cv.drawContours(img, contours, 3, (0,255,0), 1)
#cv.imshow('edge_img',edge_img)


for i in range(len(contours)):
    area = cv.contourArea(contours[i])
    print("轮廓%d的面积是:%d" % (i+1, area))
    #img_temp = np.zeros(edge_img.shape, np.uint8)
    #img_contours.append(img_temp)
    #cv.drawContours(img_contours[i], contours, i, (255, 255, 255), -1)
    #cv.imshow("%d" % i, img_contours[i])
    #计算轮廓的质心
    if i != 1:
     cnt = contours[i]
     M = cv.moments(cnt,False)

     cx = int(M['m10'] / M['m00'])
     cy = int(M['m01'] / M['m00'])
    #print("轮廓%d的质心是:(%d,%d)" % (i + 1, cx, cy))
    text = "轮廓" + str(i)+"\n"+"质心:"+str(cy)+","+str(cx)
    img=cvImgAddText(img, text, cx, cy, (255, 0, 0), 13)

#cv.imshow('edge_img1',img)

plt.subplot(221),plt.imshow(org_img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(222),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image0'), plt.xticks([]), plt.yticks([])
plt.subplot(223),plt.imshow(edge_img,cmap = 'gray')
plt.title('Edge Image1'), plt.xticks([]), plt.yticks([])
plt.subplot(224),plt.imshow(img,cmap = 'gray')
plt.title('Edge Image2'), plt.xticks([]), plt.yticks([])
plt.show()



while True:
    if ord('q') == cv.waitKey(0):
        break
cv.destroyAllWindows()
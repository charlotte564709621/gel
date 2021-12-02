import cv2 as cv
#顺时针旋转90
def rotate90CW(origiImg):
    #转置矩阵
    transpImg = cv.transpose(origiImg)
    img = cv.flip(transpImg, 1)#>0: 沿Y轴翻转；
    return img

#顺时针旋转180
def rotate180CW(origiImg):
    img = cv.flip(origiImg, -1)# <0: 沿X轴和Y轴翻转
    return img

#顺时针旋转270
#逆时针旋转90
def rotate270CW(origiImg):
    transpImg = cv.transpose(origiImg)
    img = cv.flip(transpImg, 0)#0: 沿X轴翻转；
    return img
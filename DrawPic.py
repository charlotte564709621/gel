import numpy as np
import cv2 as cv
# 创建黑色的图像
# img = np.zeros((512,512,3), np.uint8)
# # 绘制一条厚度为5的蓝色对角线
# # cv.line(img,(100,0),(100,511),(255,0,0),5)
# pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
# pts = pts.reshape((4,2))
# cv.polylines(img,[pts],False,(0,255,255))
# font = cv.FONT_HERSHEY_SIMPLEX
# cv.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2,cv.LINE_AA)
# cv.imshow('img',img)


drawing = False  # 鼠标按下为真
mode = True  # 如果为真，画矩形，按m切换为曲线
ix, iy = -1, -1
px, py = -1, -1


def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, px, py

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            cv.rectangle(img, (ix, iy), (px, py), (0, 0, 0), 0)  # 将刚刚拖拽的矩形涂黑
            cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 0)
            px, py = x, y
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 0)
        px, py = -1, -1


if __name__ == '__main__':
    img = np.zeros((512, 512, 3), np.uint8)
    cv.namedWindow('image')
    cv.setMouseCallback('image', draw_circle)
    while (1):
        cv.imshow('image', img)
        k = cv.waitKey(1) & 0xFF
        if k == ord('q'):
            break
        elif k == 27:
            break
    cv.destroyAllWindows()

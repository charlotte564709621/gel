# -*-coding:utf-8-*-
import cv2 as cv
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageDraw, ImageFont, ImageTk
import numpy as np
import re
import os
from matplotlib import pyplot as plt

class Img():
    pass

class Lane():
    pass

class Band():
    pass



def prosessing():
    #预处理
    global imgTK_lane
    blur = cv.GaussianBlur(imgCV, (5, 5), 0)
    ret3, th3 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    gauss_img = th3
    # 读取白点数量
    row, col = gauss_img.shape
    print(row, col)
    array = np.zeros(col)
    # 按列遍历
    for l in range(col):
        total = 0
        for r in range(row):
            px = gauss_img.item(r, l)
            if (px == 255):
                total = total + 1
        array[l] = total

    # 找条带分界点
    boundary = []
    for l in range(col - 1):
        if ((array[l] == 0 and array[l + 1] != 0) or (array[l] != 0 and (array[l + 1] == 0))):
            boundary.append(l)
    print(boundary)
    # 画条带，添加文字，裁剪条带
    lane_img = imgCV.copy()
    print(len(boundary))
    for i in range(0, len(boundary) - 1, 2):
        bandNo = int(i / 2 + 1)  # 条带序号
        # 画条带
        lane_img = cv.rectangle(lane_img, (boundary[i], 3), (boundary[i + 1], col), (0, 255, 0), 1)
        lane_img = cv.rectangle(lane_img, (boundary[0], 3), (boundary[1], col), (0, 255, 0), 1)
        # 标记条带
        lane_img = img_add_text(lane_img, str(bandNo), boundary[i] + 4, 5, (0, 255, 0), 15)
        cropped = imgCV[0:col, boundary[i]:boundary[i + 1]]
        File_Path = os.getcwd() + '/data/' + str(name[0])+'/lane'
        # 判断是否已经存在该目录
        if not os.path.exists(File_Path):
            # 目录不存在，进行创建操作
            os.mkdir(File_Path)  # 使用os.makedirs()方法创建多层目录
        cv.imwrite('data/'+name[0]+'/lane/lane' + str(bandNo) + '.png', cropped)

    current_image = Image.fromarray(lane_img)# 将图像转换成Image对象
    imgTK_lane = ImageTk.PhotoImage(image=current_image)  # 将image对象转换为imageTK对象
    canva.create_image(0,0,anchor = NW, image = imgTK_lane)

    for i in range(1, bandNo+1, 1):
        rdio = tk.Radiobutton(frm_rl, text="泳道"+str(i),  font=("微软雅黑", 10),
                                 variable=radioValue, value=i,command=showSelection)
        rdio.pack()


def showSelection():
    global imgTK_lane_single
    lane_img= cv.imread("data/"+str(name[0])+"/lane/lane"+str(radioValue.get())+".png")
    lane_img = cv.cvtColor(lane_img, cv.COLOR_BGR2GRAY)
    row, col = lane_img.shape
    print("lane的row和col")
    print(row,col)
    array = np.zeros(row)
    max_gray_level = 0  # 最大灰度值
    for r in range(row):
        total = 0
        for l in range(col):
            px = lane_img.item(r, l)
            if (px > max_gray_level):
                max_gray_level = px
            total += px
            array[r] = total
    print(max_gray_level)

    transp_img = cv.transpose(lane_img)
    rw_lane_img = cv.flip(transp_img, 0)#>0: 沿Y轴翻转；
    current_image = Image.fromarray(rw_lane_img )# 将图像转换成Image对象
    imgTK_lane_single = ImageTk.PhotoImage(image=current_image)  # 将image对象转换为imageTK对象
    canva2.create_image(20,50,anchor = NW, image = imgTK_lane_single)

    x = range(0, row)
    y = array[x]
    plt.plot(x, y)
    plt.xlim([0, row])
    plt.show()

def rotate90CW(origin_img):
    """
    此函数将图片顺时针旋转90度，如果需要180或270度可重复此操作
    :param origi_img: 原始图形
    :return: 旋转后的图形
    """
    transp_img = cv.transpose(origin_img)
    img = cv.flip(transp_img, 1)#>0: 沿Y轴翻转；
    return img


def img_add_text(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    """
    解决绘制中文乱码
    :param img: 原始图片
    :param text: 绘制文字
    :param left: 顶点坐标x
    :param top: 顶点坐标y
    :param textColor: 文字颜色
    :param textSize: 文字大小
    :return: opencv图片
    """
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype("font/simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv.cvtColor(np.asarray(img), cv.COLOR_RGB2BGR)

root = tk.Tk()
root.geometry('900x400+250+150')
root.title('生物分子分析系统')
# root.resizable(False, False)

def choose_pic():
    global path
    global imgTK
    path = askopenfilename()
    #文件路径
    print("打开的文件路径："+path)

    origin_img = cv.imread(path)
    global gray_img
    gray_img = cv.cvtColor(origin_img, cv.COLOR_BGR2GRAY)
    row, col = gray_img.shape
    # 放缩图片在400x400的画布上显示
    global imgCV
    if(float(row/col) > 1):
        imgCV = cv.resize(gray_img, (int(400*col/row),400))
    else:
        imgCV = cv.resize(gray_img, (400,int(400*row/col)))

    current_image = Image.fromarray(imgCV)# 将图像转换成Image对象
    imgTK = ImageTk.PhotoImage(image=current_image)  # 将image对象转换为imageTK对象
    canva.create_image(0,0,anchor = NW, image = imgTK)

    # 正则表达式读取文件名
    global name
    name = re.findall(r'[^\\/:*?"<>|\r\n]+$', path)
    name = re.findall(r'(.+?)\.', name[0])

    File_Path = os.getcwd() +'/data/'+str(name[0])
    # 判断是否已经存在该目录
    if not os.path.exists(File_Path):
        # 目录不存在，进行创建操作
        os.mkdir(File_Path) #使用os.makedirs()方法创建多层目录

    # 写回data文件夹
    cv.imwrite('data/'+str(name[0])+'/'+str(name[0])+'.png',gray_img)



menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=False)
filemenu.add_command(label="打开", command=choose_pic)
filemenu.add_command(label="保存", command=choose_pic)
filemenu.add_separator()
filemenu.add_command(label="退出", command=root.quit())
menubar.add_cascade(label="文件", menu=filemenu)


editmenu = tk.Menu(menubar, tearoff=False)
editmenu.add_command(label="裁剪", command=choose_pic)
editmenu.add_command(label="旋转", command=choose_pic)
editmenu.add_command(label="复原", command=choose_pic)
menubar.add_cascade(label="预处理", menu=editmenu)


menubar.add_command(label="分析", command=prosessing)
menubar.add_command(label="Help")



frm = tk.Frame(root)
frm.pack()

frm_l = tk.Frame(frm)
frm_r = tk.Frame(frm)
frm_l.pack(side='left')
frm_r.pack(side='right')

canva = Canvas(frm_l, width= 400, height=400, bg="gray")
canva.pack()

frm_rl = tk.Frame(frm_r)
frm_rr = tk.Frame(frm_r)
frm_rl.pack(side='left')
frm_rr.pack(side='right')
frm_rl.config(width= 100)
radioValue = tk.IntVar(frm_l)
canva2 = Canvas(frm_rr, width= 400, height=400, bg="gray")
canva2.pack()
root.config(menu=menubar)
root.mainloop()





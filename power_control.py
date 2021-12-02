import tkinter as tk
from tkinter import *
import time

flage = 0

root = tk.Tk()
root.title("设置电压")
root.geometry('500x550')
root.resizable(False, False)
v = IntVar()  # scale设置的值

label = tk.Label(root, bg="yellow", text="当前电压:", width=29, height=3,
                 font=("微软雅黑", 20, "bold"), fg='red')
label.grid(row=1)

scale = tk.Scale(root, label="电压范围", from_=0, to=2000,
                 orient=tk.HORIZONTAL, length=400, tickinterval=500,
                 resolution=1, variable=v, font=("微软雅黑", 10))
scale.grid(row=2, pady=10)

entry = tk.Entry(root, width=50, textvariable=v)
entry.configure(font=("微软雅黑", 10))
entry.grid(row=3, pady=10)


def click_button_on():
    global flage
    button_off.grid(row=4, pady=7)
    text.delete('1.0', 'end')
    value = entry.get()
    scale.set(value)
    label.config(text="当前电压:" + value)
    textstr = value + "V电压启动中...\n"
    text.insert("insert", textstr)
    text.update()

    dc = int(value) / 20  # 占空比0-100
    print(dc)

    textstr = value + "V电压已启动\n"
    text.update()
    text.insert("insert", textstr)
    flage = 1  # on

    for i in range(1, 11, 1):
        if (flage == 1):
            time.sleep(1)
            textstr = value + "V电压已启动" + str(i) + "秒\n"
            text.insert("insert", textstr)
            text.update()
            text.see(END)


def click_button_off():

    global flage
    flage = 0  # off

    button_off.grid_forget()
    button_on.grid(row=4, pady=7)
    value = entry.get()
    textstr = value + "V电压已关闭\n"
    text.insert("insert", textstr)
    text.update()
    text.see(END)


button_on = tk.Button(root, text="启动", width=50, height=3, command=click_button_on)
button_on.configure(font=("微软雅黑", 10, "bold"))
button_on.grid(row=4, pady=7)
button_off = tk.Button(root, text="关闭", width=50, height=3, command=click_button_off)
button_off.configure(font=("微软雅黑", 10, "bold"))
button_off.grid_forget()
text = tk.Text(root, bg="yellow", width=41, height=7,
               font=("微软雅黑", 15), fg='red', )
text.grid()

root.mainloop()


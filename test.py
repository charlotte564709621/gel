import pymysql
import cv2 as cv
import time
import calendar
import Rotation
# img = cv.imread('image/home.png')
# imgr = Rotation.rotate270CW(img)
# cv.imshow("imgr",imgr)
# cv.waitKey()
# cal = calendar.month(2021,11)
# print(cal)
# col = time.clock()
# print(col)
# localtime = time.asctime(time.localtime(time.time()))
# tome = time.strftime("%Y-%m-%d", time.localtime())
# print(localtime)
# print(tome)
#打开数据库
db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='gel_ele')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute()  方法执行 SQL 查询
sql = "SELECT * FROM GE_MAP"
try:
    #执行sql语句
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        map_id = row[0]
        map_name = row[1]
        voltage = row[2]
        print("id：=%s，图片名称=%s,电压=%s"%\
              (map_id, map_name,voltage))
except:
    print("error")
# 关闭数据库连接
db.close()
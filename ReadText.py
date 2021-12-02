# 导入easyocr
import easyocr
# 创建reader对象
text_list = []
reader = easyocr.Reader(['ch_sim','en'])
# 读取图像
result = reader.readtext('image/jiankangma.jpg')
# 结果
for t in result:
    print(t[1])


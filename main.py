# -*- coding:gbk -*-
from config import *
from process import *
from predict import *
from relation import *
from kp import *
import webbrowser as web
if __name__ =='__main__':
    print("开始执行 process()")
    process()  #会读测试.txt进行预测
    print("process() 执行完毕，开始执行 predict()")
    predict()
    print("predict() 执行完毕")
    triplet_result=read()
    print(f"1111111111111111:{triplet_result}")
    print('\n\n\n')
    creat_kp(triplet_result[0])  # 会将图谱数据（json格式）输出到static/output_kp/data_end.json文件  是覆盖写
    url="http://127.0.0.1:5000/view.html"
    url="http://127.0.0.1:5000/yemian"
    web.open(url)
    # content=urllib.open(url).read()
    # print(content)
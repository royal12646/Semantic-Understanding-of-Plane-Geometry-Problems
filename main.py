# -*- coding:gbk -*-
from config import *
from process import *
from predict import *
from relation import *
from kp import *
import webbrowser as web
if __name__ =='__main__':
    print("��ʼִ�� process()")
    process()  #�������.txt����Ԥ��
    print("process() ִ����ϣ���ʼִ�� predict()")
    predict()
    print("predict() ִ�����")
    triplet_result=read()
    print(f"1111111111111111:{triplet_result}")
    print('\n\n\n')
    creat_kp(triplet_result[0])  # �Ὣͼ�����ݣ�json��ʽ�������static/output_kp/data_end.json�ļ�  �Ǹ���д
    url="http://127.0.0.1:5000/view.html"
    url="http://127.0.0.1:5000/yemian"
    web.open(url)
    # content=urllib.open(url).read()
    # print(content)
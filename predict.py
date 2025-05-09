from cgitb import text
from glob import glob
import os
import random
from tkinter.font import names
import pandas as pd
from config import*
from glob import glob
from itertools import count
from operator import truediv
import re #用于多分隔符切割
from cgitb import text
import os
import random
from tkinter.font import names
import pandas as pd
from html import entities
from statistics import mode
import torch
from torch.utils import data
from seqeval.metrics import classification_report
import torch.nn as nn
from torchcrf import CRF
from glob import glob
from itertools import count
from operator import truediv
import os
from config import*
import re #用于多分隔符切割
import shutil
from process import *
#0：打标签

def setDir(filepath):
    #没有文件夹就创建，有就清空
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)



#根据标注文件生成对应关系 解析标签
def get_annotation(ann_path):
    with open(ann_path,encoding='UTF-8') as file:
        anns={}
        for line in file.readlines():
            arr=line.split()
            start=int(arr[0])
            end=int(arr[1])
            name=arr[3]#label
            #若标注太长可能会存在问题
            if end-start>50:
                continue
            anns[start]='B-'+name
            for i in range(start+1,end+1):
                anns[i]='I-'+name
        return anns

#一一对应
def get_text(txt_path):
        with open(txt_path,encoding='UTF-8') as file:
            return file.read()

#建立文字与标签的对应关系
def generate_annotation():
    full_dir=os.listdir(origin_dir)
    for i in range(len(full_dir)):
        temp=full_dir[i]
        if temp[-3:]=='txt':
            txt_path=origin_dir+full_dir[i]
            ann_path=txt_path[:-3]+'ann'
            text=get_text(txt_path)#文本
            anns=get_annotation(ann_path)#label
            #建立文本与label的对应形式
            df=pd.DataFrame({'word':list(text),'label':['O']*len(text)})

            df.loc[anns.keys(),'label']=list(anns.values())#将特殊的如B-替换进去
            #导出文件
            file_name=os.path.split(txt_path)[1]
            df.to_csv(annotation_dir+file_name[:-3]+'ann',header=None,index=None)

#拆分训练集和测试集
def split_sample(test_size=0.3):
    files=os.listdir(annotation_dir)
    for i in range (len(files)):
        files[i]=annotation_dir+files[i]
    random.seed(0)
    random.shuffle(files)
    n=int(len(files)*test_size)
    test_files=files[:n]
    train_files=files[n:]

    #合并
    merge_file(train_files,train_sample_path)
    merge_file(test_files,test_sample_path)

#合并文件
def merge_file(files,targeta_path):
    with open(targeta_path,'a',encoding='utf-8')as file:
        for f in files:
            text=open(f,encoding='utf-8').read()
            file.write(text)

#生成词表
def generate_vocab():
    df=pd.read_csv(train_sample_path,usecols=[0],names=['word'])#取汉字那一列，起名为word
    vocab_list=[word_pad,word_unk]+df['word'].value_counts().keys().tolist()
    vocab_list=vocab_list[:vocab_size]#截取掉一部分词，只保留vocab_size个词
    vocab_dict={v:k for k,v in enumerate(vocab_list)}#用enumerate生成数字作为编码k v是字
    vocab=pd.DataFrame(list(vocab_dict.items()))
    vocab.to_csv(vocab_path,header=None,index=None)#写入词表缓冲文件

#生成标签
def generate_label():
    df=pd.read_csv(train_sample_path,usecols=[1],names=['label'])#取标签那一列，起名为label
    label_list=df['label'].value_counts().keys().tolist()
    label_dict={v:k for k,v in enumerate(label_list)}#用enumerate生成数字作为编码k v是标签
    label=pd.DataFrame(list(label_dict.items()))
    label.to_csv(label_path,header=None,index=None)#写入标签表缓冲文件

#加载词表和标签表
def get_vocab():
    df=pd.read_csv(vocab_path,names=['word','id'])
    return list(df['word']),dict(df.values)

def get_label():
    df=pd.read_csv(label_path,names=['label','id'])
    return list(df['label']),dict(df.values)

#数据集处理
class Dataset(data.Dataset):
    def __init__(self,type='train',base_len=50):#base_len句长
        super().__init__()
        self.base_len=base_len
        sample_path=train_sample_path if type == 'train' else test_sample_path#判断读取训练集还是测试集
        self.df=pd.read_csv(sample_path,names=['word','label'])
        _,self.word2id = get_vocab()
        _,self.label2id = get_label()
        self.get_points()#获得切点

    #计算分割点
    def get_points(self):
        self.points=[0]#先把0这个点作为一个切割点
        i = 0          #i为之后的切割点，现在是一个临时切割点
        while True:    #建立死循环
            if i + self.base_len >=len(self.df):#若加上这个等长的切割长度后大于本身的列表长度，则将列表长度加入，并退出循环
                self.points.append(len(self.df))
                break
            elif self.df.loc[i+self.base_len,'label']=='O':#是O这个标签则可以切割
                i+=self.base_len
                self.points.append(i)
            else:#不是O标签则需要往后移一位再判读直到遇到O
                i+=1

    #文本数字化
    def __len__(self):#一共切成多少句子
        return len(self.points)-1
        #取单条数据
    def __getitem__(self,index):
        df=self.df[self.points[index]:self.points[index+1]]
        word_unk_id=self.word2id[word_unk]#获取unk对应的id
        label_o_id=self.label2id['O']#获取O对应的id
        input=[self.word2id.get(w,word_unk_id) for w in df['word']]
        target=[self.label2id.get(l,label_o_id) for l in df['label']]
        return input,target
        
 #数据校对整理
def collate_fn(batch):
    batch.sort(key=lambda x:len(x[0]),reverse=True)#按句子长度从大到小排列
    max_len=len(batch[0][0])#获得最大长度
    input=[]
    target=[]
    mask=[]
    for item in batch:
        pad_len=max_len-len(item[0])#计算要填充的长度
        input.append(item[0]+[word_pad_id]*pad_len)
        target.append(item[1]+[label_o_id]*pad_len)
        mask.append([1]*len(item[0])+[0]*pad_len)
    return torch.tensor(input),torch.tensor(target),torch.tensor(mask).bool()

def report(real_y,pre_y):
    return classification_report(real_y,pre_y)

def extract(label,text):#信息提取
    i=0
    res=[]
    while i<len(label):
        if label[i]!='O':
            prefix,name=label[i].split('-')
            start=end=i
            i+=1
            while i<len(label) and label[i]=="I-"+name:
                end=i
                i+=1
            res.append([name,text[start:end+1]])
        else:
            i+=1
    return res

def wTriangle(lst,entities):#写入提取出来的隐藏三角形实体
    lst.append(['Line_Sep',entities[0:2]])
    lst.append(['Line_Sep',entities[1:]])
    lst.append(['Line_Sep',entities[0]+entities[2]])
    lst.append(['Point_Sep',entities[0]])
    lst.append(['Point_Sep',entities[1]])
    lst.append(['Point_Sep',entities[2]])
    return lst,entities

def wPolygon(lst,entities):#写入提取出来的隐藏多边形实体
    lst.append(['Line_Sep',entities[0:2]])                 #AB
    lst.append(['Line_Sep',entities[1:3]])                 #BC
    if len(entities) == 4: #四边形ABCD
        lst.append(['Line_Sep',entities[2:]])              #CD
        lst.append(['Line_Sep',entities[0]+entities[3]])   #AD
    elif len(entities) == 5:#五边形 ABCDE
        lst.append(['Line_Sep',entities[2:4]])             #CD
        lst.append(['Line_Sep',entities[3:]])              #DE
        lst.append(['Line_Sep',entities[0]+entities[4]])   #AE
        lst.append(['Point_sep',entities[4]])              #E
    elif len(entities) == 6:#六边形 ABCDE
        lst.append(['Line_Sep',entities[2:4]])         
        lst.append(['Line_Sep',entities[3:5]])
        lst.append(['Line_Sep',entities[4:]])
        lst.append(['Line_Sep',entities[0]+entities[4]])
        lst.append(['Point_Sep',entities[4]])
        lst.append(['Point_Sep',entities[5]])
    lst.append(['Point_Sep',entities[0]])
    lst.append(['Point_Sep',entities[1]])
    lst.append(['Point_Sep',entities[2]])
    lst.append(['Point_Sep',entities[3]])
    return lst,entities

class Model(nn.Module):
    def __init__(self):
        super().__init__()#继承父类的init
        self.embed=nn.Embedding(vocab_size,embedding_dim,word_pad_id)#获取词向量
        self.lstm=nn.LSTM(
            embedding_dim,
            hidden_size,
            batch_first=True,#传过来的数据在第一维度表示的是每个batch的大小
            bidirectional=True#双向stm的设置
            )
        #Linear
        self.linear=nn.Linear(2*hidden_size,target_size)#*2的原因是双向的stm左右都有一个输出，拼在一块
        #CRF实例化
        self.crf=CRF(target_size,batch_first=True)

    def _get_lstm_feature(self,input):#lstm的特征提取
        out=self.embed(input)
        out,_=self.lstm(out)#得到一个序列（字对应的标签）
        return self.linear(out) 

    def forward(self,input,mask):#前向传播
        out=self._get_lstm_feature(input)
        return self.crf.decode(out, mask)#获取最优解

    def loss_fn(self,input,target,mask):#损失函数
        y_pred=self._get_lstm_feature(input)
        return -self.crf.forward(y_pred,target,mask,reduction='mean')#每个batch返回一个平均值



# ----------------------------model（上方）---------------------------------------------------
# ------------------------------分割------------------------------------------------------------
# ----------------------------train（下方）----------------------------------------------------------- 

def train():
    dataset = Dataset()
    loader=data.DataLoader(dataset,batch_size=100,collate_fn=collate_fn)
    model=Model()
    #优化器
    optimizer=torch.optim.Adam(model.parameters(),lr=LR)
    min_loss=0.001
    for e in range(epoch):#训练次数
        for b,(input,target,mask) in enumerate(loader):#每个batch做训练
            y_pred=model(input,mask)
            loss=model.loss_fn(input,target,mask)
            optimizer.zero_grad()#清空过往梯度
            loss.backward()#反向传播并计算当前梯度
            optimizer.step()#更新参数
        if loss.item()<min_loss:
            min_loss=loss.item()
            print('>>epoch: loss:',loss.item())
            #torch.save(model.state_dict(),model_dir+f'model_{e}.pkl')#保存模型的参数文件
            torch.save(model,model_dir+f'model3.pth')#保存模型  


# ----------------------------train（上方）---------------------------------------------------
# ------------------------------分割------------------------------------------------------------
# ----------------------------test（下方）----------------------------------------------------------- 

def test():
    dataset=Dataset("test")
    loader=data.DataLoader(dataset,batch_size=100,collate_fn=collate_fn)
    
    with torch.no_grad():#不用梯度下降
        model=torch.load(model_dir+'model3.pth')
        # model=torch.load('D:\XI\zhuomian\ToDo\几何\geometry\output\model\model2.pth')
        pre_y_list=[]
        real_y_list=[]
        id2label,_=get_label()
        for b,(input,target,mask) in enumerate(loader):
            pre_y=model(input,mask)
            loss=model.loss_fn(input,target,mask)
            print(">>batch:",b,"loss:",loss.item())
            for lst in pre_y:
                pre_y_list.append([id2label[i] for i in lst])
            for y,m in zip(target,mask):
                real_y_list.append([id2label[i] for i in y[m==True].tolist()])
            print(report(real_y_list,pre_y_list))


# ----------------------------test（上方）---------------------------------------------------
# ------------------------------分割------------------------------------------------------------
# ----------------------------predict（下方）---------------------------------------------------

def get_vocab():
    df=pd.read_csv(vocab_path,names=['word','id'])
    return list(df['word']),dict(df.values)

def get_label():
    df=pd.read_csv(label_path,names=['label','id'])
    return list(df['label']),dict(df.values)

def extract(label,text):#信息提取
    i=0
    res=[]
    while i<len(label):
        if label[i]!='O':
            prefix,name=label[i].split('-')
            start=end=i
            i+=1
            while i<len(label) and label[i]=="I-"+name:
                end=i
                i+=1
            res.append([name,text[start:end+1]])
        else:
            i+=1
    return res


def write_txtann(lst,num):
    with open(predict_ann_path+'predict'+str(num)+'.ann','a',encoding='UTF-8') as file:
        for i in range (len(lst)):
            file.write(lst[i][0]+'\t'+lst[i][1]+'\n')
    file.close()

# import pandas as pd
#
#
# def write_txtann_2(lst, num):
#     # 将列表转换为DataFrame
#     df = pd.DataFrame(lst, columns=['A', 'B'])
#
#     # 指定文件路径和文件名
#     file_path = f'{predict_ann_path}predict_csv{num}.csv'
#
#     # 将DataFrame写入文本文件，使用制表符作为分隔符
#     df.to_csv(file_path, sep='\t', index=False, encoding='UTF-8')
#

def isletter(a):
    if a >= 'a' and a <= 'z' or a >= 'A' and a <= 'Z' :
        return True
    else:
        return False

def isnumber(a):
    if a>= '0' and a<= '9' :
        return True
    elif a=='°':
        return True
    elif a=='√':
        return True
    else:
        return False

def wTriangle(lst,entities):#写入提取出来的隐藏三角形实体
    lst.append(['Line_Sep',entities[0:2]])#AB
    lst.append(['Line_Sep',entities[1:]])#BC
    lst.append(['Line_Sep',entities[0]+entities[2]])#AC

    lst=Div_Line(lst,entities[0:2],'Line_Sep')

    lst=Div_Line(lst,entities[1:],'Line_Sep')

    lst=Div_Line(lst,entities[0]+entities[2],'Line_Sep')

    return lst,entities

def wPolygon(lst,entities):#写入提取出来的隐藏多边形实体
    if len(entities) == 4: #四边形ABCD
        lst.append(['Line_Sep',entities[0:2]])                 #AB
        lst.append(['Line_Sep',entities[1:3]])                 #BC
        lst.append(['Line_Sep',entities[2:]])                  #CD
        lst.append(['Line_Sep',entities[0]+entities[3]])       #AD

        lst=Div_Line(lst,entities[0:2],'Line_Sep')

        lst=Div_Line(lst,entities[1:3],'Line_Sep')

        lst=Div_Line(lst,entities[2:],'Line_Sep')

        lst=Div_Line(lst,entities[0]+entities[3],'Line_Sep')


    elif len(entities) == 5:#五边形 ABCDE
        lst.append(['Line_Sep',entities[0:2]])                 #AB
        lst.append(['Line_Sep',entities[1:3]])                 #BC
        lst.append(['Line_Sep',entities[2:4]])                 #CD
        lst.append(['Line_Sep',entities[3:]])                  #DE
        lst.append(['Line_Sep',entities[0]+entities[4]])       #AE
        
        lst=Div_Line(lst,entities[0:2])

        lst=Div_Line(lst,entities[1:3],'Line_Sep')

        lst=Div_Line(lst,entities[2:4],'Line_Sep')

        lst=Div_Line(lst,entities[3:],'Line_Sep')

        lst=Div_Line(lst,entities[0]+entities[4],'Line_Sep')

        

    elif len(entities) == 6:#六边形 ABCDEF
        lst.append(['Line_Sep',entities[0:2]])                 #AB
        lst.append(['Line_Sep',entities[1:3]])                 #BC
        lst.append(['Line_Sep',entities[2:4]])                 #CD
        lst.append(['Line_Sep',entities[3:5]])                 #DE
        lst.append(['Line_Sep',entities[4:]])                  #EF
        lst.append(['Line_Sep',entities[0]+entities[5]])       #AF

        lst=Div_Line(lst,entities[0:2],'Line_Sep')
        
        lst=Div_Line(lst,entities[1:3],'Line_Sep')

        lst=Div_Line(lst,entities[2:4],'Line_Sep')
               
        lst=Div_Line(lst,entities[3:5],'Line_Sep')
                
        lst=Div_Line(lst,entities[4:],'Line_Sep')
     
        lst=Div_Line(lst,entities[0]+entities[5],'Line_Sep')

    return lst,entities



def write_Txt(line,dir):#写入文件 （多题目一文件拆成一题目一文件）
    with open(predict_txt_path+str(dir)+'.txt','a',encoding='UTF-8') as file:
        file.write(line)
    file.close()

def Loader_txt(dirs):
    txt_path=dirs[:-12]
    dirs=os.listdir(txt_path)#列出目录下的所有内容
    text_lst=[]
    for i in range (len(dirs)):
        d=dirs[i]#读入一个文本 eg:  d=0.txt
        if(d[-3:]=='txt'):#因为这个文件中不止有txt文件,因此要判断
            dir=txt_path+d#补全路径 eg：dir=D:/XI/zhuomian/ToDo/几何/geometry/input/0.txt
            with open(dir,encoding='UTF-8') as file:
                f=file.readlines()#逐行读入
                for line in f:
                    text_lst.append(line)
    return text_lst

def Div_Line(lst,entities,label):#从多边形中提取出来的line要增加line实体
    if len(entities)==2:
        lst.append([label,entities])
        lst.append(['Point_Sep',entities[0]])
        lst.append(['Point_Sep',entities[1]])
    return lst

def Div_Line1(lst,entities,label):#本是line只需要提出点
    if len(entities)==2:
        lst.append(['Point_Sep',entities[0]])
        lst.append(['Point_Sep',entities[1]])
    return lst

def Div_Angle(lst,entities):
    if(len(entities)==4):
        lst.append(['Line_Sep',entities[1:3]])
        lst.append(['Line_Sep',entities[2:]])

        lst=Div_Line(lst,entities[1:3],'Line_Sep')

        lst=Div_Line(lst,entities[2:],'Line_Sep')
    return lst

def seg(lst):
    new_lst=[]
    new_lst.extend(lst)
    for i in range (len(lst)):
        label=lst[i][0]
        entities=lst[i][1]
        if label=='Point' or label == 'Shape_Limit':
            continue
        else:
            new_lst.append([label,entities])
            #将提取出来的实体写入文件
            if label == 'Line' and len(entities)==2:
                new_lst=Div_Line1(new_lst,entities,"Line")
            elif label == 'Angle':
                new_lst=Div_Angle(new_lst,entities)

            elif label == 'Triangle' and len(entities)==3:   #ABC
                new_lst,_=wTriangle(new_lst,entities)
            elif label == 'Polygon' and len(entities)>3:    #多边形
                new_lst,_=wPolygon(new_lst,entities) 
            elif label == 'Value_Group':#值组合  1:2  2xy:3y
                part=re.split("[*+-/:]", entities)#拆成分句
                for j in range (len(part)):#逐个分句遍历 
                    a=''
                    k=0
                    while(k<len(part[j]) and (isnumber(part[j][k]) or isletter(part[i][j])==1)):
                        a+=part[j][k]
                        k+=1
                    if(j!=0):
                        new_lst.append(['Value_Sep',a])
                        a=''
            elif label == 'Line_Group': #线组合  AB+CD AB+2 2AB+CD 2AB^2 
                part=re.split("[*+-/:]", entities)#拆成分句
                temp_line=[]
                for j in range (len(part)):#逐个分句遍历  2AB  AB  2AB^2 
                    a=''
                    k=0
                    while(k<len(part[j]) and isnumber(part[j][k])):
                        a+=part[j][k]
                        k+=1
                    if(k!=0):
                        new_lst.append(['Value_Sep',a])
                        a=''
                    while(k<len(part[j]) and isletter(part[j][k])):#AB
                        a+=part[j][k]
                        k+=1
                    if(len(a)>0):
                        new_lst.append(['Line_Sep',a])#AB
                        temp_line.append(a)
                        a=''
                    while(k<len(part[j]) and (isnumber(part[j][k]) or part[j][k]=='^')):#^2
                        a+=part[j][k]
                        k+=1
                    if(len(a)!=0):
                        new_lst.append(['Value_Sep',a])
                        a=''
                for i in range(len(temp_line)):
                    #new_lst.append(['Line_Sep',temp_line[i]])
                    new_lst=Div_Line(new_lst,temp_line[i],'Line_Sep')
            elif label == 'Angle_Group':#角组合  ∠ABC+∠EFD  ∠ABC+2∠EFG  2∠ABC+∠EFG   2+∠ABC 
                part=re.split("[*+-/:]", entities)#拆成分句
                for j in range (len(part)):#逐个分句遍历 ∠ABC   2∠EFG 2
                    k=0
                    a=''
                    temp_angle=[]
                    while(k<len(part[j]) and isnumber(part[j][k])):
                        a+=part[j][k]
                        k+=1
                    if(k!=0):
                        new_lst.append(['Value_Sep',a])
                        a=''
                    if(k<len(part[j]) and part[j][k]=='∠'):
                        a+=part[j][k]
                        k+=1
                        while(k<len(part[j]) and isletter(part[j][k])):#∠ABC
                            a+=part[j][k]
                            k+=1
                    if(len(a)==2):#∠A
                        new_lst.append(['Angle_Sep',a])
                    elif(len(a)==4):#∠ABC
                        new_lst.append(['Angle_Sep',a])
                        temp_angle.append(a)
                        a=''
                for i in range(len(temp_angle)):
                    new_lst.append(['Angle_Sep',temp_angle[i]])
                    new_lst=Div_Angle(new_lst,temp_angle[i])
            elif label == 'Area_Group': #面积组合  S三角形ABC+2S四边形EFGH  
                part=re.split("[*+-/:]", entities)#拆成分句
                for j in range(part):
                    new_lst.append(['Area_Sep'],part[j])
            elif label == 'Perimeter_Group': #周长组合  C三角形ABC+2C四边形EFGH  
                part=re.split("[*+-/:]", entities)#拆成分句
                for j in range(part):
                    new_lst.append(['Perimeter_Sep'],part[j])
    return new_lst


# #10.28 21:17
def Deduplication(new_lst,old_lst):
    #去除同义不同形实体 AB与BA   
    for i in range (len(new_lst)):
        if(i+1==len(new_lst)):
                break
        l=new_lst[i][0]#label
        e=new_lst[i][1]#AB ABC
        if(i+1==len(new_lst)):
            break
        else:
            if(len(e)==2 and e[0]!='∠'):
                for j in range (len(old_lst)):
                    temp_e=old_lst[j][1]
                    if(len(temp_e)==2 and temp_e[0]!='∠'):
                        t1=e[1]+e[0]
                        if(t1==temp_e):
                            new_lst[i][1]=t1
                            break
            elif (len(e)==4 and e[0]=='∠'):
                for j in range(len(old_lst)):
                    temp_e=old_lst[j][1]
                    if(len(temp_e)==4 and temp_e[0]=='∠'):
                        t1=e[0]+e[3]+e[2]+e[1]
                        if(t1==temp_e):
                            new_lst[i][1]=t1
                            break
    #修改Sep label
    for i in range (len(new_lst)):
        if(i+1>len(new_lst)):
                break
        l=new_lst[i][0]#label
        e=new_lst[i][1]#AB ABC
        if(i==114):
            print(1)
        # if(i+1==len(new_lst)):
        if(i+1>len(new_lst)):
            break
        else:
            for j in range (len(old_lst)):
                if e==old_lst[j][1] and (l=='Line_Sep' or l=='Value_Sep' or l=='Point_Sep' or l=='Angle_Sep' or l=='Area_Sep' or l=='Permiter_Sep'):
                    new_lst[i][0]=old_lst[j][0]
                    break

    #对没预测出来的实体 有提出出来的实体进行 AB BA去重
    for i in range (len(new_lst)):
        if(i+1==len(new_lst)):
                break
        l=new_lst[i][0]#label
        e=new_lst[i][1]#AB ABC
        if(i+1==len(new_lst)):
            break
        else:
            if(len(e)==2 and l=='Line_Sep'):
                for j in range (i+1,len(new_lst)):
                    temp_e=new_lst[j][1]
                    temp_l=new_lst[j][0]
                    if(len(temp_e)==2 and temp_l=='Line_Sep'):
                        t1=e[1]+e[0]
                        if(t1==temp_e):
                            new_lst[j][1]=e
    return new_lst

op=['+','-','*','/',':']

def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True

_shape_limit=['等边','等腰','直角','矩形','正方形','菱形','等腰直角','等腰梯形','直角梯形','等腰直角梯形','锐角','钝角','平行四边形','凸']
#删除不合法的 例如空行\n ∠A+ +AB 中文
def Deilg(lst):
    i=0
    while i<len(lst):
        if(i==len(lst)):
            return lst
        entities=lst[i][1]
        if(entities=='\n'):
            del lst[i]
            i-=1
        if((entities[0] in op) or(entities[-1] in op)):
            del lst[i]
            i-=1
        if(is_Chinese(entities)):
            if(entities not in _shape_limit):
                del lst[i]
                i-=1
        i+=1
    return lst

def process_AOC(info):
    if(len(info)>=2):
        if info.count("S"):
            print(1)
        if info[0][1]=='S':
            if info[1][0]=="Shape_Limit":
                if info[2][0] in ["Triangle","Polygon"]:
                    info[0]=["Area",info[0][1]+info[1][1]+info[2][1]]
                    del info[1]
                    del info[1]
            else:
                if info[1][0] in ["Triangle","Polygon"]:
                    info[0]=["Area",info[0][1]+info[1][1]]
                    del info[1]
        elif info[0][1]=='C':
            if info[1][0]=="Shape_Limit":
                if info[2][0] in ["Triangle","Polygon"]:
                    info[0]=["Perimeter",info[0][1]+info[1][1]+info[2][1]]
                    del info[1]
                    del info[1]
            else:
                if info[1][0] in ["Triangle","Polygon"]:
                    info[0]=["Perimeter",info[0][1]+info[1][1]]
                    del info[1]
    return info

#！！！！！！！！！ 2023.2.23 bug：对预测错误的label更正 未完成
# def ame(lst):
#     #修正标签
#     for i in range (len(lst)):
#         label=lst[i][0]
#         entities=lst[i][1]
#         if(len(entities)==1 and label!='Point'):
#             lst[i][1]='Point'
#         elif(len(entities)==2 and label!='Line'):
#     return lst   



# def predict():
#     setDir(predict_ann_path)
#     line=Loader_txt(txt_output)#存储所有题目的一个列表
#     _,word2id=get_vocab()
#     for i in range (len(line)):
#         write_Txt(line[i],i)
#         clause=line[i].split(',')
#         entities_Line=[]
#         for j in range (len(clause)):
#             input=torch.tensor([[word2id.get(w,word_unk_id) for w in clause[j] ]])
#             mask=torch.tensor([[1]*len(clause[j])]).bool()
#             model=torch.load(model_dir+'model3.pth')
#             pre_y=model(input,mask)
#             id2label,_=get_label()
#             label=[id2label[l] for l in pre_y[0]]
#             info=extract(label,clause[j])#实体 带有标签
#             info=process_AOC(info)
#             entities_Line.extend(info)
#             # if(len(info)==1):
#             #     continue
#             # else:
#             #     entities_Line.extend(info)

#         #提取隐藏实体
#         new_info=seg(entities_Line)
#         #实体去重
#         info=Deduplication(new_info,entities_Line)
#         # info=Deduplication(new_info,info)
#         #删除有问题实体
#         info=Deilg(info)
#         write_txtann(info,i)


def predict():
    setDir(predict_ann_path)
    text=Loader_txt(txt_output)
    _,word2id=get_vocab()

    for i in range (len(text)):
        write_Txt(text[i],i)
        input=torch.tensor([[word2id.get(w,word_unk_id) for w in text[i] ]])
        mask=torch.tensor([[1]*len(text[i])]).bool()
        model=torch.load(model_dir+'model3.pth')
        pre_y=model(input,mask)
        id2label,_=get_label()
        label=[id2label[l] for l in pre_y[0]]

        info=extract(label,text[i])#实体 带有标签
        #修正标签
        #new_info=ame(info)
        #提取隐藏实体
        new_info=seg(info)
        #实体去重
        info=Deduplication(new_info,info)
        # info=Deduplication(new_info,info)
        #删除有问题实体
        info=Deilg(info)
        print(f"info:{type(info)}")
        write_txtann(info,i)
        # write_txtann_2(info,i)

    

# if __name__=='__main__':
#     # process()
#     #建立对应关系
#     generate_annotation()

#     #拆分样本集
#     split_sample()
    
#     #生成词表
#     generate_vocab()
   
#     #生成标签表
#     generate_label()

#     dataset = Dataset()
#     loader=data.DataLoader(dataset,batch_size=100,collate_fn=collate_fn)

#     model=Model()
#     input=torch.randint(0,3000,(100,10))#维度大小是100*10 每个batch100个句子 每个句子长度10

#     train()
    # test()
    # process()
    # predict()
    
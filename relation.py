import os
import csv
import re
from turtle import numinput
from config import *
import shutil
from predict import *
from process import *

#关系提取，实体提取（有group）

def Init_csv(file_name):
    with open(triplet_path+file_name.replace('ann','csv'),'w',newline='',encoding="utf-8")as f:
        csv_writer=csv.writer(f)
        head1=['entity_1','label_1','relation_1','entity_2','label_2','relation_2','entity_3','label_3']
        csv_writer.writerow(head1)
        f.close()

def WriteTriplet(temp,triplet,triplet_1,file_name):
    if temp not in triplet:
        triplet.append(temp)
        with open(triplet_path+file_name.replace('ann','csv'),'a',newline='',encoding="utf-8")as f:
            csv_writer=csv.writer(f)
            csv_writer.writerow(temp)
        if len(temp)>5:
            triplet_1.append([temp[0],temp[1],temp[2],temp[3],temp[4]])
            triplet_1.append([temp[0],temp[1],temp[2],temp[6],temp[7]])
            triplet_1.append([temp[3],temp[4],temp[5],temp[6],temp[7]])
        else:
            triplet_1.append(temp)

def Constructs_Relation(ey,num,triplet,triplet_1,file_name):
    r='constructs'
    n,m=num,num+1
    while n<len(ey):
        if ey[n][1] in ['Triangle','Polygon']:
            while m<len(ey) and ey[m+1][1] in ['Line','Line_Sep']:
                temp=[ey[m][0],ey[m][1],r,ey[n][0],ey[n][1]]
                WriteTriplet(temp,triplet,triplet_1,file_name)
                m+=1

        elif ey[n][1] in ['Angle','Angle_Sep'] and len(ey[n][0])>=4:
            while m<len(ey) and ey[m+1][1] in ['Line','Line_Sep']:
                temp=[ey[m][0],ey[m][1],r,ey[n][0],ey[n][1]]
                WriteTriplet(temp,triplet,triplet_1,file_name)
                m+=1     

        elif ey[n][1] in ['Line','Line_Sep']:
            while m<len(ey) and ey[m][1] in ['Point','Point_Sep']:
                temp=[ey[m][0],ey[m][1],r,ey[n][0],ey[n][1]]
                WriteTriplet(temp,triplet,triplet_1,file_name)
                m+=1     

        elif ey[n][1] == 'Angle_Group':
            while m<len(ey) and ey[m][1] in ['Angle','Angle_Sep','Value','Value_Sep']:
                if m+1<len(ey) and ey[m][1]in ['Angle','Angle_Sep'] and ey[m+1][1] in ['Line','Line_Sep']:
                    break
                temp=[ey[m][0],ey[m][1],r,ey[n][0],ey[n][1]]
                WriteTriplet(temp,triplet,triplet_1,file_name)
                m+=1          

        elif ey[n][1]=='Line_Group':
            while m<len(ey) and ey[m][1] in ['Line','Line_Sep','Value','Value_Sep']:
                if m+1<len(ey) and ey[m][1]in ['Line','Line_Sep'] and ey[m+1][1] in ['Point','Point_Sep']:
                    break
                temp=[ey[m][0],ey[m][1],r,ey[n][0],ey[n][1]]
                WriteTriplet(temp,triplet,triplet_1,file_name)
                m+=1

        elif ey[n][1]=='Value_Group':
            while m<len(ey) and ey[m][1] in ['Value','Value_Sep']:
                temp=[ey[m][0],ey[m][1],r,ey[n][0],ey[n][1]]
                WriteTriplet(temp,triplet,triplet_1,file_name)
                m+=1 

        elif ey[n][1]=='Area_Group':
            while m<len(ey) and ey[m][1] in ['Area','Area_Sep']:
                temp=[ey[m][0],ey[m][1],r,ey[n][0],ey[n][1]]
                WriteTriplet(temp,triplet,triplet_1,file_name)
                m+=1         

        elif ey[n][1]=='Perimeter_Group':
            while m<len(ey) and ey[m][1] in ['Perimeter','Perimeter_Sep']:
                temp=[ey[m][0],ey[m][1],r,ey[n][0],ey[n][1]]
                WriteTriplet(temp,triplet,triplet_1,file_name)
                m+=1         
        n,m=m,m+1

def relation(text,ey,file_name):
    newtext=text.split(',')
    triplet=[]
    triplet_1=[['entity_1','label_1','relation_1','entity_2','label_2']]
    n,m,z=0,1,2
    for clause in newtext:
        r,t='',''
        if re.search('交.*?于', clause)!=None:
            r='intersectPoint'
            t='intersect'
        elif re.search('⊥.*?于', clause)!=None:
            r='verticalPoint'
            t='vertical'
        elif clause.find("平行")!=-1:
            r='parallel'
            s=ey[n][1]+'+'+ey[m][1]
            if s in ['Shape_Limit+Triangle','Shape_Limit+Polygon']:
                r='shapelimit'
        elif clause.find('⊥')!=-1:
            r='vertical'
        elif clause.find('交')!=-1:
            r='intersect'
        elif clause.find('平分')!=-1:
            r='eqSplit'    
        elif clause.find('中点')!=-1:
            r='eqSplit'               
        elif clause.find('=')!=-1:
            r='equals'
            if ey[m][1]=='Value':
                r='values'
        elif clause.find('>')!=-1:
            r='bigger'
        elif re.search('在.*?上', clause)!=None:
            r='on'
        elif re.search('在.*?内', clause)!=None:
            r='in'
        elif re.search('是.*?高',clause)!=None:
            r='height'
        elif clause.find('~')!=-1:
            r='similar'
        elif clause.find('≌')!=-1:
            r='congruent'         
        else:
            s=ey[n][1]+'+'+ey[m][1]
            if s in ['Shape_Limit+Triangle','Shape_Limit+Polygon']:
                r='shapelimit'
            elif s in ['Shape_Limit+Angle']:
                r='anglelimit'

        if r=='':
            n,m,z=n+1,m+1,z+1
        elif r!='':
            if ey[n][1] == 'Shape_Limit' and r != 'shapelimit':
                temp=[ey[n][0],ey[n][1],'shapelimit',ey[m][0],ey[m][1]]
                WriteTriplet(temp,triplet,triplet_1,file_name)
                n,m=n+1,m+1
            if ey[m][1] == 'Shape_Limit' and r != 'shapelimit':
                temp=[ey[m][0],ey[m][1],'shapelimit',ey[m+1][0],ey[m+1][1]]
                WriteTriplet(temp,triplet,triplet_1,file_name)
                m+=1
        if t!='':
            temp=[ey[z][0],ey[z][1],r,ey[n][0],ey[n][1],t,ey[m][0],ey[m][1]]
            WriteTriplet(temp,triplet,triplet_1,file_name)
            n,m,z=z+1,z+2,z+3
        elif r!='':
            temp=[ey[n][0],ey[n][1],r,ey[m][0],ey[m][1]]
            WriteTriplet(temp,triplet,triplet_1,file_name)
            n,m,z=m+1,m+2,m+3
    Constructs_Relation(ey,n,triplet,triplet_1,file_name)
    return triplet_1     
    
def read():
    setDir(triplet_path)
    triplet_sum=[]
    for file_name in os.listdir(text_path):
        if file_name[-4:]=='.txt':
            with open(text_path+file_name, "r",encoding="utf-8") as f:
                text=f.read()
                text = text.replace('\n', '') 
                f.close()
            ey=[]
            file_name=file_name.replace('txt','ann')
            with open(entity_path+'predict'+file_name,"r",encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.replace('\n', '') 
                    arr=line.split('\t')
                    if arr!=['']:
                        ey.append([arr[1],arr[0]])
            Init_csv(file_name)
            triplet_sum.append(relation(text,ey,file_name))
    return triplet_sum

def setDir(filepath):
    #没有文件夹就创建，有就清空
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)

# if __name__ == "__main__":
#     process()
#     predict()
#     triplet_result=read()
#     with open(txt_input,'r',encoding="utf-8")as f1:
#         txt=f1.readlines()
#     with open(txt_output,'r',encoding="utf-8")as f2:
#         txt_after=f2.readlines()
#     with open('D:/XI/zhuomian/ToDo/几何/geometry/result.txt','w',encoding="utf-8")as w:
#         i=0
#         for file_name in os.listdir(triplet_path):
#             w.write(txt[int(file_name[:-4])])
#             w.write(txt_after[int(file_name[:-4])]+'\n')
#             with open(triplet_path+file_name,'r',encoding="utf-8")as f3:
#                 reader=csv.reader(f3)
#                 header_row=next(reader)
#                 for j in reader:
#                     for k in range(len(j)):
#                         w.write(j[k])
#                         w.write('\t')
#                     w.write('\n')
#             w.write('\n\n\n\n')
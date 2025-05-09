#0：打标签
Label={
    'O','Shape_Limit','Point','Point_Sep','Line','Line_Sep',
    'Angle','Triangle','Polygon','Value','Area','Perimeter'
    }
from glob import glob
from itertools import count
from operator import truediv
import os
from config import*
import re #用于多分隔符切割
import shutil
# from process import*
def write(a,b,c,d,dir):
    with open(origin_dir+str(dir)+'.ann','a',encoding='UTF-8') as file:
    #with open(origin_dir+'test.ann','a',encoding='UTF-8') as file:
        file.write(str(a)+'\t'+str(b)+'\t'+c+'\t'+d+'\n')
    file.close()

def write_txt(line,dir):#写入文件 （多题目一文件拆成一题目一文件）
    with open(origin_dir+str(dir)+'.txt','a',encoding='UTF-8') as file:
        file.write(line)
    file.close()
    
def isletter(k):
    if k >= 'a' and k <= 'z':
        return 1
    elif k >= 'A' and k <= 'Z' :
        return 2
    else:
        return 0

def isnumber(k):
    if k>= '0' and k<= '9' :
        return True
    elif k=='°':
        return True
    elif k=='√':
        return True
    else:
        return False

#Area or Perimeter 处理 ABC:AEF ABC+AEF - * / :  
def AOP(a,i,j,index,part,flag):
    if(j+6<len(part[i]) and part[i][j]=='△' ):#S△ABC C△ABC
        a+=part[i][j:j+4]
        j+=4
        index+=4
        flag+=1
    elif(j+6<len(part[i]) and (part[i][j:j+2]=='矩形'or part[i][j:j+2]=='菱形')):
        a+=part[i][j:j+6]
        j+=6
        index+=6
        flag+=1
    elif(j+7<len(part[i]) and (part[i][j:j+3]=='四边形' or part[i][j:j+3]=='正方形'or part[i][j:j+3]=='长方形')):
        a+=part[i][j:j+7]
        j+=7
        index+=7
        flag+=1
    elif(j+8<len(part[i]) and part[i][j:j+4]=='凸四边形'): 
        a+=part[i][j:j+8]
        j+=8
        index+=8
        flag+=1
    elif(j+8<len(part[i]) and part[i][j:j+5]=='平行四边形'):  
        a+=part[i][j:j+9]
        j+=9
        index+=9
        flag+=1
    return a,i,j,index,part,flag

#判断有无指数部分
def Index(a,i,j,index,part):
    if(j<len(part[i]) and part[i][j]=='^'):
        a+=part[i][j]
        j+=1
        index+=1
        while(j<len(part[i]) and isnumber(part[i][j])):
            a+=part[i][j]
            j+=1
            index+=1
    return a,i,j,index,part

def Identify(line):
    global temp_name#d为写入文本的路径
    global index#用来记录当前读取到得字符的位置，用来获得end 和 start
    part=line.split(',')#拆成分句
    i=0
    while i < len(part):#逐个分句遍历
        index+=1#补充'，'占有的位置
        j=0
        while j < len(part[i]):#对分句中的逐个字符遍历
            a=""
            f=False
            #读字母进入 判断
            # 1、点 面积 周长  SABC:SBCD=1:2 SABC+SBCD SABC-SCEF SABC*SBGD SABC/SONH 同理C……
            # 2、线 AB:CD AB+CD AB-CD AB*CD AB/CD
            # 3、三角形 正方形 四边形 五边形 六边形  eg:abc是三角形
            if isletter(part[i][j])==2:
                f=True
                a+=part[i][j]
                j+=1
                index+=1
                while (j<len(part[i]) and isletter(part[i][j])==2) :
                    a+=part[i][j]
                    j+=1
                    index+=1
                    if(j+1>len(part[i])):
                        break
                
                if len(a)==1:#点 面积 周长
                    if (a=='S' or a=='C'):# 点S 面积Area  周长Perimeter
                        flag=0 #用于标识是否识别出是面积和周长 若没有则S C就是一个点
                        a,i,j,index,part,flag=AOP(a,i,j,index,part,flag)
                        #判断有无指数
                        a,i,j,index,part=Index(a,i,j,index,part)
                        if(flag==0):
                            write(index-len(a), index-1, a, "Point",temp_name)
                        else:#S△ABC   C△ABC
                            flag1=0#用于判断是只有一个S△ABC 还是有 S△ABC+S△BCD  S△AB+12 等情况
                            #S△ABC+S△EFGH C△ABC+C四边形EFGH 情况：
                            while(j<len(part[i]) and (part[i][j]=='+' or part[i][j]=='-' or part[i][j]=='*' or part[i][j]=='/' or part[i][j]==':')):
                                a+=part[i][j:j+1]#  a:=S△ABC+
                                j+=1
                                index+=1
                                flag1=1
                                #a:= S△ABC+S四边形EFGH
                                if(j<len(part[i]) and part[i][j]==a[0]):
                                    a+=part[i][j:j+1]#  a:= S△ABC+S
                                    j+=1
                                    index+=1
                                    a,i,j,index,part,flag=AOP(a,i,j,index,part,flag) #a:= S三角形ABC+S四边形EFGH
                                    #判断有无指数
                                    a,i,j,index,part=Index(a,i,j,index,part)
                                #a:= S三角形ABC+12   a:= S三角形ABC+12S四边形EGHF
                                elif(j<len(part[i]) and isnumber(part[i][j])): #a:= S三角形ABC+
                                    a+=part[i][j:j+1]#  a:= S三角形ABC+1
                                    j+=1
                                    index+=1
                                    while(j<len(part[i]) and isnumber(part[i][j])):
                                        a+=part[i][j:j+1]#  a:= S三角形ABC+12
                                        j+=1
                                        index+=1
                                    if(j<len(part[i]) and part[i][j]==a[0]):
                                        a+=part[i][j:j+1]#  a:= S三角形ABC+12S
                                        j+=1
                                        index+=1
                                        a,i,j,index,part,flag=AOP(a,i,j,part,flag) #a:= S三角形ABC+12S四边形EFGH
                                        #判断有无指数
                                        a,i,j,index,part=Index(a,i,j,index,part)
                            if(flag1==0):#说明只有一个S三角形ABC C三角形ABC
                                if a[0]=='S':
                                    write(index-len(a), index-1, a, "Area",temp_name)#Area
                                elif a[0]=='C':
                                    write(index-len(a), index-1, a, "Perimeter",temp_name)#Perimeter
                            else:#说明有 S三角形ABC+S三角形EGF 等组合情况
                                if a[0]=='S':
                                    write(index-len(a), index-1, a, "Area_Group",temp_name)#Area_Group
                                elif a[0]=='C':
                                    write(index-len(a), index-1, a, "Perimeter_Group",temp_name)#Perimeter_Group
                    else:#除了S、C以外的单个字母
                        write(index-len(a), index-1, a, "Point",temp_name)
                    # write(index-len(a), index-1, a, "Point",temp_name)

                elif len(a)==2:#线 线运算
                    #判断有无指数
                    a,i,j,index,part=Index(a,i,j,index,part)
                    flag=0#用于标记是组合形式还是单独线形式
                    while(j<len(part[i]) and (part[i][j]=='+' or part[i][j]=='-' or part[i][j]=='*' or part[i][j]=='/' or part[i][j]==':')):
                        a+=part[i][j]
                        j+=1
                        index+=1
                        flag=1
                        while(j<len(part[i]) and isnumber(part[i][j])):#AB+12
                            a+=part[i][j]
                            j+=1
                            index+=1
                            if(j+1>len(part[i])):
                                break
                        while (j<len(part[i]) and isletter(part[i][j])) :#AB+CD:  AB+2CD 
                            a+=part[i][j]
                            j+=1
                            index+=1
                            if(j+1>len(part[i])):
                                break
                        #判断有无指数
                        a,i,j,index,part=Index(a,i,j,index,part)
                    if(flag==0):    
                        write(index-len(a), index-1, a, "Line",temp_name)#Line AB
                    elif(flag==1):
                        write(index-len(a), index-1, a, "Line_Group",temp_name)#Line AB:AC
                elif len(a)==3:#三角形
                    write(index-len(a), index-1, a, "Triangle",temp_name)#Triangle ABC
                elif len(a)>=4:#多边形：（四边）（五边）（六边）
                    write(index-len(a),index-1,a,"Polygon",temp_name)#Polygon ABCD
            a=""
            if(j+1>len(part[i])):
                continue

            #判断角 读∠进去 给abc打angle   
            if part[i][j]=='∠':
                f=True
                a+=part[i][j]
                j+=1
                index+=1
                flag=0
                while (j<len(part[i]) and isletter(part[i][j])):#∠
                    a+=part[i][j]                               #∠A ∠ABC
                    j+=1
                    index+=1
                #判断有无指数
                a,i,j,index,part=Index(a,i,j,index,part)
                while(j<len(part[i]) and (part[i][j]=='+' or part[i][j]=='-' or part[i][j]=='*' or part[i][j]=='/' or part[i][j]==':')):#∠A+
                    flag=1                                                                                                             
                    a+=part[i][j]
                    j+=1
                    index+=1
                    while(j<len(part[i]) and isnumber(part[i][j])): #∠A+2   ∠A+
                        a+=part[i][j]
                        j+=1
                        index+=1
                    if(j==len(part[i])):
                        break
                    if(j<len(part[i][j]) and part[i][j]=='∠'):#∠A+2∠    ∠A+∠
                        a+=part[i][j]
                        j+=1
                        index+=1
                        while(j<len(part[i]) and isletter(part[i][j])==2):#∠A+2∠EGG  ∠A+∠E
                            a+=part[i][j]
                            j+=1
                            index+=1
                        #判断有无指数
                        a,i,j,index,part=Index(a,i,j,index,part)
                if(flag==0):
                    write(index-len(a), index-1, a, "Angle",temp_name)#Angle   ∠ABC
                elif(flag==1):
                    write(index-len(a), index-1, a, "Angle_Group",temp_name)#Angle_group   ∠ABC
            a=""
            if(j+1>len(part[i])):
                continue  

            #判断值 读数字进入 给数字打value  或者读小写字母进入  xy
            if isnumber(part[i][j]) or isletter(part[i][j])==1:
                f=True
                a+=part[i][j]
                j+=1
                index+=1
                flag=0
                while (j<len(part[i]) and isnumber(part[i][j])):#12
                    a+=part[i][j]
                    j+=1
                    index+=1
                while(j<len(part[i]) and isletter(part[i][j])==1):#2xy
                    a+=part[i][j]
                    j+=1
                    index+=1
                while(j<len(part[i]) and isletter(part[i][j])==2):#2AB
                    flag=3
                    a+=part[i][j]
                    j+=1
                    index+=1
                #判断有无指数
                a,i,j,index,part=Index(a,i,j,index,part)
                while(j<len(part[i]) and (part[i][j]=='∠' or part[i][j]=='+' or part[i][j]=='-' or part[i][j]=='*' or part[i][j]=='/' or part[i][j]==':')):#1:   1
                    a+=part[i][j]
                    j+=1
                    index+=1
                    while (j<len(part[i]) and (isnumber(part[i][j]) or isletter(part[i][j])==1)):#1:2 1+2  12:2xy
                        flag=1#纯值 12+4 12/6 Value_Group  
                        a+=part[i][j]
                        j+=1
                        index+=1
                    if(j<len(part[i]) and part[i][j-1]=='∠'):
                        while(j<len(part[i]) and isletter(part[i][j])==2):#2∠ABC+∠EFG+4∠E
                            flag=2#有角度 12+4∠ANC   Angle_Group
                            a+=part[i][j]
                            j+=1
                            index+=1
                    counter=0#记录下面是2AB 还是2S三角形ABC
                    while(j<len(part[i]) and isletter(part[i][j])):
                        counter+=1
                        a+=part[i][j]
                        j+=1
                        index+=1
                    if(counter==2):
                        flag=3#有线 2+2AB
                    elif(counter==1 and j<len(part[i]) and (part[i][j-1]=='S' or part[i][j-1]=='C')):#可能是 2+S三角形ABC 情况
                        if(part[i][j-1]=='S'):
                            flag=4#有面积 2+2S三角形ABC
                        elif(part[i][j-1]=='C'):
                            flag=4#有周长 2+2C三角形ABC
                        a+=part[i][j]
                        j+=1
                        index+=1
                        a,i,j,index,part,_=AOP(a,i,j,index,part,flag)
                    #判断有无指数
                    # a,i,j,index,part=Index(a,i,j,index,part)

                if(flag==0):
                    write(index-len(a),index-1,a,"Value",temp_name)
                elif(flag==1):
                    write(index-len(a),index-1,a,"Value_Group",temp_name)
                elif(flag==2):
                    write(index-len(a),index-1,a,"Angle_Group",temp_name)
                elif(flag==3):
                    write(index-len(a),index-1,a,"Line_Group",temp_name)
                elif(flag==4):
                    write(index-len(a),index-1,a,"Area_Group",temp_name)
                elif(flag==5):
                    write(index-len(a),index-1,a,"Perimeter_Group",temp_name)
            if(j+1>len(part[i])):
                continue  

            #锐角 钝角 等边 等腰 直角 菱形 梯形 矩形：
            if(j+2<len(part[i]) and part[i][j:j+2]=="锐角" or part[i][j:j+2]=="钝角" or part[i][j:j+2]=="等边" or part[i][j:j+2]=="等腰" or part[i][j:j+2]=="直角" or part[i][j:j+2]=="菱形" or part[i][j:j+2]=="梯形" or part[i][j:j+2]=="矩形"):
                f=True
                j+=2
                index+=2
                if(j+2<len(part[i]) and part[i][j:j+2]=="梯形"):
                    j+=2
                    index+=2
                    write(index-4,index-1,part[i][j-4:j],"Shape_Limit",temp_name)
                elif(j+3<len(part[i]) and part[i][j:j+3]=="直角"):
                    j+=3
                    index+=3
                    write(index-5,index-1,part[i][j-4:j],"Shape_Limit",temp_name)
                else:
                    write(index-2,index-1,part[i][j-2:j],"Shape_Limit",temp_name)
            if(j+1>len(part[i])):
                continue

            #正方形 
            if(j+3<len(part[i]) and part[i][j:j+3]=="正方形"):
                f=True
                j+=3
                index+=3
                write(index-3,index-1,'正方形',"Shape_Limit",temp_name)
            if(j+1>len(part[i])):
                continue


            #凸四边形 读凸
            if(j+1<len(part[i]) and part[i][j:j+2]=="凸" ):
                f=True
                j+=1
                index+=1
                write(index-4,index-1,"凸","Shape_Limit",temp_name)                
            if(j+1>len(part[i])):
                continue

            #平行四边形
            if(j+5<len(part[i]) and part[i][j:j+5]=="平行四边形" ):
                f=True
                j+=5
                index+=5
                write(index-5,index-1,"平行四边形","Shape_Limit",temp_name)                
            if(j+1>len(part[i])):
                continue

            if(f==False):
                j+=1
                index+=1
        i+=1

#导入文本
def get_text(txt_path):
    dirs=os.listdir(txt_path)#列出目录下的所有内容
    full_path=[]
    global temp_name #用来拆文件的时候给文件按顺序从0开始命名
    global index #用来记录当前读取到得字符的位置，用来获得end 和 start
    for i in range(len(dirs)):#逐文件读入
        d=dirs[i]#读入一个文本 eg:  d=0.txt
        if(d[-3:]=='txt'):#因为这个文件中不止有txt文件,因此要判断
            dir=txt_path+d#补全路径 eg：dir=D:/XI/zhuomian/ToDo/几何/geometry/input/0.txt
            full_path.append(dir)
            with open(dir,encoding='UTF-8') as file:
                f=file.readlines()#逐行读入
                for line in f:
                    index=-1
                    write_txt(line,temp_name)#将一个文件多个题目拆成一个文件一个题目
                    dir=dir[:-3]+'ann'
                    Identify(line)
                    temp_name+=1
            file.close()

def setDir(filepath):
    #没有文件夹就创建，有就清空
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)

if __name__=='__main__':
    # process()
    global temp_name #用于之后拆题目成一个个文本时给新文本命名
    temp_name=0
    get_text(txt_output[:-12])
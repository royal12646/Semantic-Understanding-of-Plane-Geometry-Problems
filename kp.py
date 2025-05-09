from config import *
import csv
import pandas as pd
import json

def creat_kp(str_data):
    entity = './static/output_kp/entity.csv'  # 最终的实体文件的csv文件
    name = []
    des = []
    st = []
    with open(path_b, encoding='utf-8') as file:
        content = file.read()
        content1 = content.rstrip().split()  # rstrip删除空行
        for i in range(len(content1)):
            if i % 2 == 0:
                des.append(content1[i])
            else:
                name.append(content1[i])
        for a, b in zip(name, des):
            x = {}
            x['name'] = a
            x['des'] = b
            st.append(x)
        # print(type(st))

        un_st=[]
        for i in st:
            if i not in un_st:
                un_st.append(i)
        # print(un_st)

    with open(entity, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'des'])
        for nl in un_st:
            writer.writerow(nl.values())

    # 5、生成relationship_1文件
    # 打开原数据
    relational_data=[]
    print(str_data)

    for i in range(len(str_data)):
        relational_data.append([str_data[i][0], str_data[i][2], str_data[i][3]])
    # print(relational_data)
    # 另存为relation_1文件
    with open(path_d, 'w', newline='', encoding="utf-8") as c:
        writer3 = csv.writer(c)
        for row in relational_data:
            writer3.writerow(row)


    # 更改relation_1的表头
    df = pd.read_csv(path_d, header=0, encoding="utf-8")
    df.columns = ["source", "name", "target"]
    df.to_csv(path_d, index=False)

    # 将csv文件内数据读出
    ngData = pd.read_csv(entity, encoding='utf-8')
    ngList = []  # 准备一个列表，把新列的数据存入其中
    for row in ngData.iterrows():  # 遍历数据表，计算每一位名字的长度
        ngList.append('category')
    ngData['category'] = ngData['des']  # 注明列名，就可以直接添加新列
    ngData.to_csv(entity, index=False)  # 把数据写入数据集，index=False表示不加索引
    # 注意这里的ngData['length']=ngList是直接在原有数据基础上加了一列新的数据，也就是说现在的ngData已经具备完整的3列数据
    # 不用再在to_csv中加mode=‘a’这个参数，实现不覆盖添加。

    cate = []
    ca = []
    for row in ngData.iterrows():
        cate = ngData['category']
        ca = cate

    for i in range(len(cate)):
        if cate[i] == 'Shape_Limit':
            cate.values[i] = 0
        elif cate[i] == 'Point':
            cate.values[i] = 1
        elif cate[i] == 'Point_Sep':
            cate.values[i] = 2
        elif cate[i] == 'Line':
            cate.values[i] = 3
        elif cate[i] == 'Line_Sep':
            cate.values[i] = 4
        elif cate[i] == 'Angle':
            cate.values[i] = 5
        elif cate[i] == 'Angle_Sep':
            cate.values[i] = 6
        elif cate[i] == 'Value':
            cate.values[i] = 7
        elif cate[i] == 'Value_Sep':
            cate.values[i] = 8
        elif cate[i] == 'Triangle':
            cate.values[i] = 9
        elif cate[i] == 'Polygon':
            cate.values[i] = 10
        elif cate[i] == 'Area':
            cate.values[i] = 11
        elif cate[i] == 'Perimeter':
            cate.values[i] = 12
        elif cate[i] == 'Line_Group':
            cate.values[i] = 13
        elif cate[i] == 'Angle_Group':
            cate.values[i] = 14
        elif cate[i] == 'Area_Group':
            cate.values[i] = 15
        elif cate[i] == 'Perimeter_Group':
            cate.values[i] = 16
        elif cate[i] == 'Value_Group':
            cate.values[i] = 17

    ngData['category'] = cate  # 注明列名，就可以直接添加新列
    ngData.to_csv(entity, index=False)  # 把数据写入数据集，index=False表示不加索引
    ngData1 = pd.read_csv(entity)
    

    # 生成json文件
    # 生成实体的实体的json文件
    fo1 = open(entity, "r", encoding='utf-8')  # 打开csv文件
    ls1 = []
    for line in fo1:
        line = line.replace("\n", "")  # 将换行换成空
        arr = line.split(",")
        if '0' <= arr[2] <= '9':
            arr[2] = int(arr[2])
        ls1.append(arr)

    fo1.close()  # 关闭文件流

    fw = open(entity_end, "w", encoding="utf8")  # 打开json文件
    for i in range(1, len(ls1)):  # 遍历文件的每一行内容，除了列名
        ls1[i] = dict(zip(ls1[0], ls1[i]))  # ls[0]为列名，所以为key,ls[i]为value,
        # zip()是一个内置函数，将两个长度相同的列表组合成一个关系对
    json.dump(ls1[1:], fw, sort_keys=True, indent=4, ensure_ascii=False)
    fw.close()

    fo2 = open(path_d, "r", encoding='utf-8')  # 打开csv文件
    ls2 = []
    for line in fo2:
        line = line.replace("\n", "")  # 将换行换成空
        ls2.append(line.split(","))  # 以，为分隔符
    fo2.close()  # 关闭文件流
    fw = open(relation_end, "w", encoding="utf8")  # 打开json文件
    for i in range(1, len(ls2)):  # 遍历文件的每一行内容，除了列名
        ls2[i] = dict(zip(ls2[0], ls2[i]))  # ls[0]为列名，所以为key,ls[i]为value,
        # zip()是一个内置函数，将两个长度相同的列表组合成一个关系对
    json.dump(ls2[1:], fw, sort_keys=True, indent=4, ensure_ascii=False)
    fw.close()

    # 合并两个entity_end.json、relation_end.json文件
    # 打开实体文件
    with open(entity_end, 'r', encoding='utf-8') as f1:
        entity = json.load(f1)
        # print(e)

    # 打开关系文件
    with open(relation_end, 'r', encoding='utf-8') as f2:
        relation = json.load(f2)
        print(relation)

    # 合并两个文件
    fw = open(data_end, "w", encoding="utf-8")  # 打开json文件
    categories = [
        {"name": "Shape_Limit"},
        {"name": "Point"}, {"name": "Point_Sep"},
        {"name": "Line"}, {"name": "Line_Sep"},
        {"name": "Angle"}, {"name": "Angle_Sep"},
        {"name": "Value "}, {"name": "Value_Sep"},
        {"name": "Triangle "}, {"name": "Polygon "},
        {"name": "Area"}, {"name": "Perimeter "},
        {"name": "Line_Group"}, {"name": "Angle_Group"},
        {"name": "Area_Group"}, {"name": "Perimeter_Group"},
        {"name": "Value_Group"}
    ]

    ls2 = {"nodes": entity, "links": relation, 'categories': categories}
    json.dump(ls2, fw, sort_keys=True, indent=4, ensure_ascii=False)
    fw.close()

    with open(data_end, 'r', encoding='utf-8') as ff:
        data_line = json.load(ff)
        # print(data_line)
        # print(type(data_line))

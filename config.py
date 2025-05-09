#config.py 配置文件

txt_input = "测试.txt"  #原题目（多道未拆分）
txt_output = "./test/disposed.txt"

origin_dir = "./input/"  #原始文件夹
annotation_dir = "./output/annotation/"  #标注后文件夹

train_sample_path = "./output/train_sample2.ann"  #训练集
test_sample_path = "./output/test_sample2.ann"  #测试集

vocab_path = "./output/vocab2.ann"
label_path = "./output/label2.ann"

predict_ann_path = "./output/predict/"  #存储预测出来的实体路径
predict_txt_path = "./output/predict/"  #存储预测出来的实体路径(原题目)

word_pad = "<PAD>"  #用于填充使得句子长度相同
word_unk = "<UNK>"  #训练集中不包含的

word_pad_id = 0  #pad对应的id
label_o_id = 0  #o对应的id
vocab_size = 3000  #词表大小
word_unk_id = 1

embedding_dim = 100  #词向量维度
hidden_size = 256  #BilSTM输出的隐藏层维度
target_size = 29  #经过全连接层后的输出向量维度(多少种label：B-Line之类的)
LR = 1e-3  #学习率
epoch = 5000  #训练次数

model_dir = "./mnt/disk1/LY/Semantic-Understanding-of-Plane-Geometry-Problems/" #存储学习后得到的模型

# 关系提取路径
#实现知识图谱三元式路径
#triplet_path_1="/output_1/"
# 预处理后题目路径
text_path = predict_txt_path
# 实体路径
entity_path = predict_ann_path
# 三元式路径
triplet_path = "./output_triplet/"

#知识图谱路径
path_b = './output/predict/predict0.ann'  # 实体文件
# path_d = './output_kp/relationship_1.csv'  # 关系links的文件
# entity_end = "./output_kp/entity_end.json"  # 最终的实体json文件
# relation_end = "./output_kp/relation_end.json"  # 最终的关系json文件
# data_end = "./output_kp/data_end.json"  # 合并实体和关系的json文件的最终需要生成图谱的数据文件
path_d = './static/output_kp/relationship_1.csv'  # 关系links的文件
entity_end = "./static/output_kp/entity_end.json"  # 最终的实体json文件
relation_end = "./static/output_kp/relation_end.json"  # 最终的关系json文件
data_end = "./static/output_kp/data_end.json"  # 合并实体和关系的json文件的最终需要生成图谱的数据文件

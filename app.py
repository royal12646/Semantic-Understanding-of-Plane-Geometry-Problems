from flask import Flask, jsonify, redirect, url_for
from flask import render_template
from flask import request

from kp import *
from relation import *

app = Flask(__name__, template_folder='static/templates')


@app.route("/yemian")
def yemian():  #主页面
    return render_template('yemian.html')


@app.route("/process", methods=["POST"])
def process():  # 处理并显示
    abnormal = True
    data = request.json
    t = data['input']
    print(t)
    process_text(t)
    predict()
    triplet_result = read()
    creat_kp(triplet_result[0])

    with open(r'./mnt/disk1/LY/Semantic-Understanding-of-Plane-Geometry-Problems/output/predict/0.txt', 'r', encoding='utf-8') as f:
        quesion_result = f.read()

    with open(r'./mnt/disk1/LY/Semantic-Understanding-of-Plane-Geometry-Problems/output/predict/predict0.ann', 'r', encoding='utf-8') as f:
        graphData = f.readlines()

    # 处理 graphData 为表格格式
    table_data = []
    for line in graphData:
        if line.strip():  # 确保非空行
            item = line.strip().split("\t")  # 按制表符分割
            if len(item) == 2:  # 只处理有两列的行
                table_data.append({"type": item[0], "name": item[1]})

    # 返回的数据包括问题结果和表格数据
    result = {
        "quesion_result": quesion_result,
        "graph_result": table_data  # 将处理后的表格数据添加到返回结果中
    }

    return jsonify(result)


@app.route("/conf", methods=["POST", "GET"])  #处理
def conf():
    return render_template('result.html')

@app.route("/")
def index():
    return render_template("yemian.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

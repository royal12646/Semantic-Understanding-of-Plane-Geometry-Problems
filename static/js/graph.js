// 提交按钮逻辑
document.getElementById("submit").addEventListener("click", function () {
    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            input: document.getElementById("topic").value
        })
    }).then(response => response.json())
        .then(data => {
            showGraph();
            document.getElementById("question_processed").innerHTML = "处理题目结果："+data.quesion_result;

            // 创建表格来展示 graph_result
            const graphDataDiv = document.getElementById("graphData");
            graphDataDiv.innerHTML = ""; // 清空旧数据

            const table = document.createElement('table');
            const headerRow = document.createElement('tr');
            headerRow.innerHTML = "<th>类型</th><th>名称</th>";
            table.appendChild(headerRow);

            data.graph_result.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>${item.type}</td><td>${item.name}</td>`;
                table.appendChild(row);
            });

            graphDataDiv.appendChild(table);
        });
});



    // 处理重置按钮
    document.getElementById("reset").addEventListener("click", function () {
        // 清空问题与图谱数据
        document.getElementById("topic").value = ''; // 清空输入框
        document.getElementById("question_processed").innerHTML = ''; // 清空已显示的结果
        document.getElementById("graphData").innerHTML = ''; // 清空图数据
        clearGraph(); // 清空图谱
    });

    // 清空图谱函数
    function clearGraph() {
        var chartDom = document.getElementById('main');
        var myChart = echarts.init(chartDom);
        myChart.clear(); // 清空图表
    }

    // 显示图谱函数
    function showGraph() {
        var chartDom = document.getElementById('main');
        var myChart = echarts.init(chartDom);
        var option;

        fetch('static/output_kp/data_end.json')
            .then(response => {
                if (!response.ok) {
                    throw new Error('网络响应不是一个 200 响应');
                }
                return response.json(); // 解析 JSON 数据
            })
            .then(graph => {
                option = {
                    title: {
                        text: '知识图谱',
                        subtext: '',
                        top: 'bottom',
                        left: 'right'
                    },
                    tooltip: {
                        formatter: function (x) {
                            return x.data.des;
                        }
                    },
                    legend: [{
                        data: graph.categories.map(a => a.name)
                    }],
                    series: [{
                        name: 'Les Miserables',
                        type: 'graph',
                        layout: 'force',
                        edgeSymbolSize: [2, 10],
                        edgeSymbol: ['circle', 'arrow'],
                        symbolSize: 60,
                        focusNodeAdjacency: false,
                        data: graph.nodes,
                        links: graph.links,
                        categories: graph.categories,
                        roam: true,
                        draggable: true,
                        label: {
                            normal: {
                                show: true,
                                textStyle: {}
                            }
                        },
                        lineStyle: {
                            color: 'source',
                            width: 2,
                            curveness: 0,
                            show: true
                        },
                        emphasis: {
                            focus: 'adjacency',
                            lineStyle: {
                                width: 10
                            }
                        },
                        force: {
                            repulsion: 2500,
                            edgeLength: [60, 100]
                        },
                        edgeLabel: {
                            normal: {
                                show: true,
                                formatter: function (x) {
                                    return x.data.name;
                                }
                            }
                        }
                    }]
                };
                myChart.setOption(option); // 绘制图表
            })
            .catch(error => console.error('获取数据时出现问题:', error));
    }
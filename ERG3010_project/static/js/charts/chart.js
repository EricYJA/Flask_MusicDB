$.getJSON('../static/melody_data.json', function (_data){
	var data=[];
	$.each(_data, function(index, d){
		data.push({"value":[d[0],d[1],d[2]],"name":d[3]});
	})
	getChart1(data);
});

$.getJSON('../static/sentiment_data.json', function (_data){
	getChart2(_data);
});

$.getJSON('../static/broad_adj.json', function (_data){
	getChart3(_data);
});

$.getJSON('../static/broad_scene.json', function (_data){
	getChart4(_data);
});

$.getJSON('../static/broad_time.json', function (_data){
	getChart5(_data);
});

function getChart1(data){
	var myChart = echarts.init(document.getElementById('704fa6a2209d412491311b26793969d6'), 'light', {renderer: 'canvas'});

	var option = {
		"title": [{
			"text": "Melody Analysis",
			"subtext": "of all music the database",
			"left": "center",
			"top": "auto",
			"textStyle": {
				"color": "#FB6107",
				"fontSize": 30
			},
			"subtextStyle": {
				"fontSize": 14
			}
		}],
		"toolbox": {
			"show": true,
			"orient": "vertical",
			"left": "95%",
			"top": "center",
			"feature": {
				"saveAsImage": {
					"show": true,
					"title": "save as image"
				},
				"restore": {
					"show": true,
					"title": "restore"
				},
				"dataView": {
					"show": true,
					"title": "data view"
				}
			}
		},
		"series_id": 6606500,
		"tooltip": {
			"trigger": "item",
			"triggerOn": "mousemove|click",
			"axisPointer": {
				"type": "line"
			},
			"textStyle": {
				"fontSize": 14,
				"color": "#fff"
			},
			"backgroundColor": "rgba(50,50,50,0.7)",
			"borderColor": "#333",
			"borderWidth": 0
		},
		"series": [{
			"type": "scatter3D",
			"data": data,
			"label": {
				"normal": {
					"show": false,
					"position": "top",
					"textStyle": {
						"fontSize": 12
					}
				},
				"emphasis": {
					"show": true,
					"textStyle": {
						"fontSize": 12
					}
				},
			},
			"itemStyle": {
				"opacity": 3
			}
		}],
		"legend": [{
			"data": [
			],
			"selectedMode": "multiple",
			"show": true,
			"left": "center",
			"top": "top",
			"orient": "horizontal",
			"textStyle": {
				"fontSize": 12
			}
		}],
		"animation": true,
		"xAxis3D": {
			"name": "PCA1",
			"nameGap": 20,
			"nameTextStyle": {
				"fontSize": 16
			},
			"type": "value",
			"axisLabel": {
				"margin": 8,
				"interval": "auto"
			}
		},
		"yAxis3D": {
			"name": "PCA2",
			"nameGap": 20,
			"nameTextStyle": {
				"fontSize": 16
			},
			"type": "value",
			"axisLabel": {
				"margin": 8,
				"interval": "auto"
			}
		},
		"zAxis3D": {
			"name": "PCA3",
			"nameGap": 20,
			"nameTextStyle": {
				"fontSize": 16
			},
			"type": "value",
			"axisLabel": {
				"margin": 8
			}
		},
		"grid3D": {
			"boxWidth": 100,
			"boxHeight": 100,
			"boxDepth": 100,
			"viewControl": {
				"autoRotate": true,
				"autoRotateSpeed": 10,
				"rotateSensitivity": 1
			}
		},
		"color": [
			"#c23531",
			"#2f4554",
			"#61a0a8",
			"#d48265",
			"#749f83",
			"#ca8622",
			"#bda29a",
			"#6e7074",
			"#546570",
			"#c4ccd3",
			"#f05b72",
			"#ef5b9c",
			"#f47920",
			"#905a3d",
			"#fab27b",
			"#2a5caa",
			"#444693",
			"#726930",
			"#b2d235",
			"#6d8346",
			"#ac6767",
			"#1d953f",
			"#6950a1",
			"#918597",
			"#f6f5ec"
		],
		"visualMap": {
			"type": "continuous",
			"min": 0,
			"max": 100,
			"text": [
				"high",
				"low"
			],
			"textStyle": {},
			"inRange": {
				"color": [
					"#313695",
					"#4575b4",
					"#74add1",
					"#abd9e9",
					"#e0f3f8",
					"#ffffbf",
					"#fee090",
					"#fdae61",
					"#f46d43",
					"#d73027",
					"#a50026"
				]
			},
			"calculable": true,
			"splitNumber": 5,
			"orient": "vertical",
			"left": "left",
			"top": "bottom",
			"showLabel": true
		}
	};

	myChart.setOption(option);
}

function getChart2(data){
	var myChart = echarts.init(document.getElementById('5ff03a3ab5b14ad4bb54ce1da2753ce6'), 'light', {renderer: 'canvas'});

	var option = {
		"title": [
			{
				"text": "Sentiment",
				"left": "auto",
				"top": "auto",
				"textStyle": {
					"color": "#274C77",
					"fontSize": 20
				},
				"subtextStyle": {
					"fontSize": 12
				}
			}
		],
		"toolbox": {
			"show": true,
			"orient": "vertical",
			"left": "95%",
			"top": "center",
			"feature": {
				"saveAsImage": {
					"show": true,
					"title": "save as image"
				},
				"restore": {
					"show": true,
					"title": "restore"
				},
				"dataView": {
					"show": true,
					"title": "data view"
				}
			}
		},
		"series_id": 7970580,
		"tooltip": {
			"trigger": "axis",
			"triggerOn": "mousemove|click",
			"axisPointer": {
				"type": "line"
			},
			"textStyle": {
				"fontSize": 14
			},
			"backgroundColor": "rgba(50,50,50,0.7)",
			"borderColor": "#333",
			"borderWidth": 0
		},
		"series": [
			{
				"type": "themeRiver",
				"name": [
					"Pos",
					"Neg"
				],
				"data": data,
				"label": {
					"normal": {
						"show": true,
						"position": "top",
						"textStyle": {
							"fontSize": 12
						}
					},
					"emphasis": {
						"show": true,
						"textStyle": {
							"fontSize": 12
						}
					}
				},
				"seriesId": 7970580
			}
		],
		"legend": [
			{
				"data": [
					"Pos",
					"Neg"
				],
				"selectedMode": "multiple",
				"show": true,
				"left": "center",
				"top": "top",
				"orient": "horizontal",
				"textStyle": {
					"fontSize": 15,
					"color": "#274C77"
				}
			}
		],
		"animation": true,
		"singleAxis": {
			"type": "time"
		},
		"color": [
			"#c23531",
			"#2f4554",
			"#61a0a8",
			"#d48265",
			"#749f83",
			"#ca8622",
			"#bda29a",
			"#6e7074",
			"#546570",
			"#c4ccd3",
			"#f05b72",
			"#ef5b9c",
			"#f47920",
			"#905a3d",
			"#fab27b",
			"#2a5caa",
			"#444693",
			"#726930",
			"#b2d235",
			"#6d8346",
			"#ac6767",
			"#1d953f",
			"#6950a1",
			"#918597",
			"#f6f5ec"
		],
		"dataZoom": [
			{
				"show": true,
				"type": "slider",
				"start": 50,
				"end": 100,
				"orient": "horizontal"
			}
		]
	};
	myChart.setOption(option);
}

function getChart3(data){
	var myChart = echarts.init(document.getElementById('dcc7393e722e4c5fa3e08ae3fa462880'), 'light', {renderer: 'canvas'});

	var option = {
		"title": [
			{
				"text": "ADJ LIST",
				"left": "auto",
				"top": "auto",
				"textStyle": {
					"fontSize": 18,
					"color":"#FFF"
				},
				"subtextStyle": {
					"fontSize": 12
				}
			}
		],
		"toolbox": {
			"show": true,
			"orient": "vertical",
			"left": "95%",
			"top": "center",
			"feature": {
				"saveAsImage": {
					"show": true,
					"title": "save as image"
				},
				"restore": {
					"show": true,
					"title": "restore"
				},
				"dataView": {
					"show": true,
					"title": "data view"
				}
			}
		},
		"series_id": 13262,
		"tooltip": {
			"trigger": "item",
			"triggerOn": "mousemove|click",
			"axisPointer": {
				"type": "line"
			},
			"textStyle": {
				"fontSize": 14,
				"color":"#FFF"
			},
			"backgroundColor": "rgba(50,50,50,0.7)",
			"borderColor": "#333",
			"borderWidth": 0
		},
		"series": [
			{
				"type": "bar",
				"coordinateSystem": "polar",
				"stack": "stack",
				"name": "ADJ",
				"itemStyle": {
					"color":"#FB6107",
				},
				"data": data
			}
		],
		"legend": [
			{
				"data": [
					"ADJ"
				],
				"selectedMode": "multiple",
				"show": true,
				"left": "center",
				"top": "top",
				"orient": "horizontal",
				"textStyle": {
					"fontSize": 12,
					"color":"#FFF"
				}
			}
		],
		"animation": true,
		"angleAxis": {},
		"radiusAxis": {
			"show": true,
			"type": "category",
			"color":"#FFF",
			"axisLine": {
				"show": true,
				"lineStyle": {
					"normal": {
						"width": 1,
						"opacity": 1,
						"curveness": 0,
						"type": "solid",
						"color":"#FFF"
					}
				}
			},
			"axisLabel": {
				"rotate": 0,
				"color":"#FFF"
			},
			"nameTextStyle":{
				"color":"#FFF"
			},
			"z": 50
		},
		"polar": {},
		"color": [
			"#c23531",
			"#2f4554",
			"#61a0a8",
			"#d48265",
			"#749f83",
			"#ca8622",
			"#bda29a",
			"#6e7074",
			"#546570",
			"#c4ccd3",
			"#f05b72",
			"#ef5b9c",
			"#f47920",
			"#905a3d",
			"#fab27b",
			"#2a5caa",
			"#444693",
			"#726930",
			"#b2d235",
			"#6d8346",
			"#ac6767",
			"#1d953f",
			"#6950a1",
			"#918597",
			"#f6f5ec"
		]
	};
	myChart.setOption(option);
}

function getChart4(data){
	var myChart = echarts.init(document.getElementById('b97ca027168b43a885acb151c4991089'), 'light', {renderer: 'canvas'});
	var option = {
		"title": [
			{
				"text": "SCENE LIST",
				"left": "auto",
				"top": "auto",
				"textStyle": {
					"fontSize": 18,
					"color":"#FFF"
				},
				"subtextStyle": {
					"fontSize": 12
				}
			}
		],
		"toolbox": {
			"show": true,
			"orient": "vertical",
			"left": "95%",
			"top": "center",
			"feature": {
				"saveAsImage": {
					"show": true,
					"title": "save as image"
				},
				"restore": {
					"show": true,
					"title": "restore"
				},
				"dataView": {
					"show": true,
					"title": "data view"
				}
			}
		},
		"series_id": 2322713,
		"tooltip": {
			"trigger": "item",
			"triggerOn": "mousemove|click",
			"axisPointer": {
				"type": "line"
			},
			"textStyle": {
				"fontSize": 14,
				"color":"#FFF"
			},
			"backgroundColor": "rgba(50,50,50,0.7)",
			"borderColor": "#333",
			"borderWidth": 0
		},
		"series": [
			{
				"type": "bar",
				"coordinateSystem": "polar",
				"stack": "stack",
				"name": "SCENE",
				"data": data
			}
		],
		"legend": [
			{
				"data": [
					"SCENE"
				],
				"selectedMode": "multiple",
				"show": true,
				"left": "center",
				"top": "top",
				"orient": "horizontal",
				"textStyle": {
					"fontSize": 12,
					"color":"#FFF"
				}
			}
		],
		"animation": true,
		"angleAxis": {},
		"radiusAxis": {
			"show": true,
			"type": "category",
			"axisLine": {
				"show": true,
				"lineStyle": {
					"normal": {
						"width": 1,
						"opacity": 1,
						"curveness": 0,
						"type": "solid",
						"color":"#FFF"
					}
				}
			},
			"axisLabel": {
				"rotate": 0,
				"color":"#FFF"
			},
			"z": 50
		},
		"polar": {},
		"color": [
			"#c23531",
			"#2f4554",
			"#61a0a8",
			"#d48265",
			"#749f83",
			"#ca8622",
			"#bda29a",
			"#6e7074",
			"#546570",
			"#c4ccd3",
			"#f05b72",
			"#ef5b9c",
			"#f47920",
			"#905a3d",
			"#fab27b",
			"#2a5caa",
			"#444693",
			"#726930",
			"#b2d235",
			"#6d8346",
			"#ac6767",
			"#1d953f",
			"#6950a1",
			"#918597",
			"#f6f5ec"
		]
	};
	myChart.setOption(option);
}

function getChart5(data){
	var myChart = echarts.init(document.getElementById('a81bba8742d9445486c2996cab457e87'), 'light', {renderer: 'canvas'});

	var option = {
		"title": [
			{
				"text": "TIME LIST",
				"left": "auto",
				"top": "auto",
				"textStyle": {
					"fontSize": 18,
					"color":"#FFF"
				},
				"subtextStyle": {
					"fontSize": 12
				}
			}
		],
		"toolbox": {
			"show": true,
			"orient": "vertical",
			"left": "95%",
			"top": "center",
			"feature": {
				"saveAsImage": {
					"show": true,
					"title": "save as image"
				},
				"restore": {
					"show": true,
					"title": "restore"
				},
				"dataView": {
					"show": true,
					"title": "data view"
				}
			}
		},
		"series_id": 6136542,
		"tooltip": {
			"trigger": "item",
			"triggerOn": "mousemove|click",
			"axisPointer": {
				"type": "line"
			},
			"textStyle": {
				"fontSize": 14,
				"color":"#FFF"
			},
			"backgroundColor": "rgba(50,50,50,0.7)",
			"borderColor": "#333",
			"borderWidth": 0
		},
		"series": [
			{
				"type": "bar",
				"coordinateSystem": "polar",
				"stack": "stack",
				"name": "TIME",
				"data": data
			}
		],
		"legend": [
			{
				"data": [
					"TIME"
				],
				"selectedMode": "multiple",
				"show": true,
				"left": "center",
				"top": "top",
				"orient": "horizontal",
				"textStyle": {
					"fontSize": 12,
					"color":"#FFF"
				}
			}
		],
		"animation": true,
		"angleAxis": {
			"show": true,
			"type": "category",
			"clockwise": true,
			"startAngle": 90,
			"boundaryGap": true,
			"splitLine": {
				"show": true,
				"lineStyle": {
					"normal": {
						"width": 1,
						"opacity": 1,
						"curveness": 0,
						"type": "solid",
						"color":"#FFF"
					}
				}
			},
			"axisLine": {
				"show": true,
				"lineStyle": {
					"normal": {
						"width": 1,
						"opacity": 1,
						"curveness": 0,
						"type": "solid",
						"color":"#FFF"
					}
				}
			},
			"axisLabel": {
				"interval": 0,
				"color":"#FFF"
			},
			"z": 50
		},
		"radiusAxis": {
			"show": true,
			"type": "category",
			"axisLine": {
				"show": true,
				"lineStyle": {
					"normal": {
						"width": 1,
						"opacity": 1,
						"curveness": 0,
						"type": "solid",
						"color":"#FFF"
					}
				}
			},
			"axisLabel": {
				"rotate": 0,
				"color":"#FFF"
			},
			"z": 50
		},
		"polar": {},
		"color": [
			"#c23531",
			"#2f4554",
			"#61a0a8",
			"#d48265",
			"#749f83",
			"#ca8622",
			"#bda29a",
			"#6e7074",
			"#546570",
			"#c4ccd3",
			"#f05b72",
			"#ef5b9c",
			"#f47920",
			"#905a3d",
			"#fab27b",
			"#2a5caa",
			"#444693",
			"#726930",
			"#b2d235",
			"#6d8346",
			"#ac6767",
			"#1d953f",
			"#6950a1",
			"#918597",
			"#f6f5ec"
		]
	};
	myChart.setOption(option);
}
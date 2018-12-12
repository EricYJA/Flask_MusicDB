$.getJSON('../static/melody_data.json', function (_data){
	var data=[];
	$.each(_data, function(index, d){
		data.push({"value":[d[0],d[1],d[2]],"name":d[3]});
	})
	getChart1(data);
});
function getChart1(data){
	var myChart_704fa6a2209d412491311b26793969d6 = echarts.init(document.getElementById(
		'704fa6a2209d412491311b26793969d6'), 'light', {
		renderer: 'canvas'
	});

	var option_704fa6a2209d412491311b26793969d6 = {
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
	myChart_704fa6a2209d412491311b26793969d6.setOption(option_704fa6a2209d412491311b26793969d6);
}
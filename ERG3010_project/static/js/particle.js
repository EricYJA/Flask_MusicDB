sigma.classes.graph.addMethod('neighbors', function(nodeId) {
	var k,
		neighbors = {},
		index = this.allNeighborsIndex[nodeId] || {};

	for (k in index)
	neighbors[k] = this.nodesIndex[k];

	return neighbors;
});

sigma.parsers.json('../static/file.json', 
	{
		renderer: {
			container: document.getElementById('container'),
			type: 'canvas',
		},
		// renderer: {
		// 	container: document.getElementById('container'),
		// 	type: 'canvas',
		// },
		settings: {
			defaultNodeColor: '#FB6107',
			defaultLabelColor: '#FFFFFF',
			minEdgeSize: 0.1,
			maxEdgeSize: 3
		}
	},

	function(s){
		s.addRenderer({
			container: document.getElementById('container-p'),
			type: 'canvas',
			settings: {
				defaultNodeColor: '#FB6107',
				labelColor: 'node',
				labelThreshold:3,
				defaultLabelSize: 12,
				minEdgeSize: 0.1,
				maxEdgeSize: 3

			}
		  });
		s.graph.nodes().forEach(function (n) {
			n.x = Math.random() * 300;
			n.y = Math.random() * 300;
			n.ax = Math.random() * 2 -1;
			n.ay = Math.random() * 2 -1;
		});
		s.graph.edges().forEach(function(e){
			e.type = "curve";
		})
		s.refresh();
		// We first need to save the original colors of our
		// nodes and edges, like this:
		s.graph.nodes().forEach(function (n) {
			n.originalColor = n.color;
		});
		s.graph.edges().forEach(function (e) {
			e.originalColor = e.color;
		});

		// When a node is clicked, we check for each node
		// if it is a neighbor of the clicked one. If not,
		// we set its color as grey, and else, it takes its
		// original color.
		// We do the same for the edges, and we only keep
		// edges that have both extremities colored.
		s.bind('clickNode', function (e) {
			var nodeId = e.data.node.id,
				toKeep = s.graph.neighbors(nodeId);
			toKeep[nodeId] = e.data.node;

			s.graph.nodes().forEach(function (n) {
				if (toKeep[n.id]){
					n.color = n.originalColor;
				}
				else{
					n.color = '#111';
				}
			});

			s.graph.edges().forEach(function (e) {
				if (toKeep[e.source] && toKeep[e.target])
					e.color = e.originalColor;
				else
					e.color = '#111';
			});

			// Since the data has been modified, we need to
			// call the refresh method to make the colors
			// update effective.
			s.refresh();
		});

		// When the stage is clicked, we just color each
		// node and edge with its original color.
		s.bind('clickStage', function (e) {
			s.graph.nodes().forEach(function (n) {
				n.color = n.originalColor;
			});

			s.graph.edges().forEach(function (e) {
				e.color = e.originalColor;
			});

			// Same as in the previous event:
			s.refresh();
		});

		setInterval(function() {
			s.graph.nodes().forEach(function(n) {
				n.x += n.ax;
				n.y += n.ay;
				n.ax *= (n.x > 300 || n.x < -300) ? -1 : 1;
				n.ay *= (n.y > 300|| n.y < -300) ? -1 : 1;
				n.x = (n.x > 300) ? 300 : n.x;
				n.x = (n.x < -300) ? -300 : n.x;
				n.y = (n.y > 300) ? 300 : n.y;
				n.y = (n.y < -300) ? -300 : n.y;
			});
			s.refresh();
		}, 100);
	}
);	
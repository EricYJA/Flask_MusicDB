def html_generate(song_name,song_id):
	GEN_HTML = "templates\song_list.html"
	f = open(GEN_HTML,'w')
	table_content = ""
	for i in range(len(song_id)/2):
		table_content = table_content + """
		<tr>
				<td><a id="%s" href="{{ 'song/%s' }}" >%s</a></td>
				<td><a id="%s" href="{{ 'song/%s' }}" >%s</a></td>
		</tr>"""%(song_id[2*i-1],song_name[2*i-1],song_name[2*i-1],song_id[i*2],song_name[i*2],song_name[i*2])

	if len(song_id) % 2 == 1:
		table_content = table_content + """
		<tr>
			<td><a id="%s" href="{{ 'song/%s' }}" >%s</a></td>
		</tr>"""%(song_id[len(song_id)-1],song_name[len(song_id)-1],song_name[len(song_id)-1])
	
	messsage = """
	<!DOCTYPE html>
	<html class="no-js" lang="en">

	<head>
		<!--- basic page needs ================================================== -->
		<meta charset="utf-8">
		<title>MusicDB</title>
		<meta name="description" content="ERG3010 Final Project">
		<meta name="author" content="DiBiaoZuiWen">

		<!-- mobile specific metas ================================================== -->
		<meta name="viewport" content="width=device-width, initial-scale=1">

		<!-- CSS ================================================== -->
		<link rel="stylesheet" href="../static/css/font-awesome/css/font-awesome.min.css">
		<link rel="stylesheet" href="../static/css/base.css">
		<link rel="stylesheet" href="../static/css/demo.css">
		<link rel="stylesheet" href="../static/css/main.css">
		<link rel="stylesheet" href="../static/css/singer-list.css">
		<!--- script ================================================== -->
		<script src="../static/js/modernizr.js"></script>
		<script src="../static/js/jquery-3.2.1.min.js"></script>

		<!-- favicons ================================================== -->
		<link rel="shortcut icon" href="../static/favicon1.ico" type="image/x-icon">
		<link rel="icon" href="../static/favicon1.ico" type="image/x-icon">
	</head>

	<body>
		<form method="get" action={{url_for('singer')}} >
			<table id="song-table" border="0">
			%s
			</table>
		</form>
	</body>
	"""%(table_content)

	f.write(messsage)
	f.close()
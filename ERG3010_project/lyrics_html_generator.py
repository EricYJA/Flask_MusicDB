def lyrics_html_generate(txt):
	lyrics = txt.splitlines()
	GEN_HTML = "ERG3010_project/templates/lyrics.html"
	f = open(GEN_HTML,'w')
	lyrics_content = ""
	for i in range(len(lyrics)):
		lyrics_content = lyrics_content + """
		<p>
    	%s
		</p>"""%(lyrics[i])
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
		<link rel="stylesheet" href="../static/css/lyrics.css">
		<!--- script ================================================== -->
		<script src="../static/js/modernizr.js"></script>

		<!-- favicons ================================================== -->
		<link rel="shortcut icon" href="../static/favicon1.ico" type="image/x-icon">
		<link rel="icon" href="../static/favicon.ico" type="image/x-icon">
	</head>
	<body>
	%s
	</body>
	"""%(lyrics_content)

	f.write(messsage)
	f.close()
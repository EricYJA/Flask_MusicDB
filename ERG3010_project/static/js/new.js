$(document).ready(function(){
	$("#user-input").focus(function(){
		$("#user i").css("color", "#FB6107");
	});
	$("#user-input").blur(function(){
		$("#user i").css("color", "white");
	});

	$("#password-input").focus(function(){
		$("#key i").css("color", "#FB6107");
	});	
	$("#password-input").blur(function(){
		$("#key i").css("color", "white");
	});	 
	$("#login").click(function(){
		$('.login').css("opacity","1");
	});
	$("#close").click(function(){
		$('.login').css("opacity","0");
	});

	$(".album-image div").click(function(){
		var id = $(this).attr("id");
		var player = '<iframe id="play-album" frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=110 src="//music.163.com/outchain/player?type=1&id='+id+'&auto=1&height=90"></iframe>'
		$("#player").empty();
		$("#player").append(player);
		$("#play-album").css("display","none");
		$("#play-album").fadeIn(3000);
	});

	$(".zoom").click(function(){
		$('<div id="overlay-image"></div>').insertAfter("main");
		$("#overlay-image").fadeIn();
		var src = $(this).attr("src");
		$('<div class="zoom-image" style="background-image:url('+src+');"></div>').insertAfter("#overlay-image");
		$(".zoom-image").fadeIn();

		$("#overlay-image").click(function(){
			$(this).remove();
			$(".zoom-image").remove();
		});
		$(".zoom-image").click(function(){
			$("#overlay-image").remove();
			$(this).remove();
		});
	});

	$("#song h1 span").click(function(){
		var id = $(this).attr("id");
		var player = '<iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=86 src="//music.163.com/outchain/player?type=2&id='+id+'&auto=1&height=66"></iframe>'
		$("#player").append(player);
		$("#play-album").css("display","none");
		$("#play-album").fadeIn(3000);
	});

	$("#container-zoom").click(function(){
		$('<div id="overlay-image" style="background: rgba(0,0,0,0.9);"></div>').insertAfter("main");
		$("#overlay-image").fadeIn();
		$("#container-p").fadeIn();
		$("#overlay-image").click(function(){
			$("#container-p").css("display","none")
			$(this).remove();
		});
	});
});

if (window != top) {
	top.location.href = location.href; 
}



/* Namespace Spin */ spin = {

createHelix:function(){
	$('#efforia').drawSVG('static/svg/interface.svg',$.e.h-40,$.e.h-40);
	$.e.widthNow = $('body').width();
},

holdHelix:function(event){
	event.preventDefault();
	$.e.holding = true; $.e.clicked = true; 
},

releaseHelix:function(event){
	event.preventDefault(); 
	$.e.holding = false;
	$.e.value = true; 
	if(!$.e.clicked){
		$.e.marginTop += margin;
		$.e.marginMax = -$('.block,.mini').height()*$.e.marginFactor;
		$('#Grade').translate(0,$.e.marginTop);
		//Verificacao do topo
		if($.e.marginTop > 0 && margin > 0){
			$('#Grade').translate(0,$.e.marginTop); $.e.marginTop = 0;
			setTimeout(function(){$('#Grade').translate(0,$.e.marginTop);},1000);
		//Verificacao da base
		}else if($.e.marginMax-$.e.marginTop > 0 && margin < 0){
			$('#Grade').translate(0,$.e.marginTop); $.e.marginTop = $.e.marginMax;
			setTimeout(function(){$('#Grade').translate(0,$.e.marginTop);},1000);
		}
		setTimeout(function(){ $.e.angle = 0; $('#efforia').rotate($.e.angle);},1000);
	}
	if (!$.e.holding && $.e.clicked && $.e.value) {
		$.fn.hideMenus();
	}
},

moveHelix:function(event){
	event.preventDefault();
	if ($.e.holding) {
		$.e.clicked = false;
		x = event.pageX; y = event.pageY;
		if ($.e.velocity < 0) $.e.velocity = -$.e.velocity;
		// Sentido antihorario
		if ($.e.velocity >= $.e.last) {
			margin = -$('.block,.mini').height()*2;
			$.e.last = $.e.velocity;
			$.e.velocity = -(Math.atan(y/x))*$.e.acceleration;
		// Sentido horario
		} else if ($.e.velocity < $.e.last) {
			margin = $('.block,.mini').height()*2;
			$.e.last = $.e.velocity;
			$.e.velocity = Math.atan(y/x)*$.e.acceleration;
		}
		$.e.angle += $.e.velocity;
		$('#efforia').rotate($.e.angle);
	}
},

hideHelix:function(event){
	event.preventDefault();
	if(!$.e.openedMenu){
		$.e.openedMenu = true;
		$('#Canvas').hide();
	}else{
		$.e.openedMenu = false;
		$('#Canvas').show();
	}
}

}

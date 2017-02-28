var CurrentTime = new Date()
var CurrentYear = CurrentTime.getFullYear()-13

var uploader = {
	type:'POST',
	imageMaxWidth:1280,
	imageMaxHeight:720,
	allowUploadOriginalImage:true,
	beforeSend:function(){ $('.send').button('loading'); },
	success:function(data){
		if($('.description').length > 0){
			$.post('images',{'description':$('.description').val()},function(data){
				$.fn.showMosaic();
			});	
		} else {
			$.fn.showMosaic();
		}
	}}
var datepick = { 
	format:'dd/mm/yyyy',
	language:'pt-BR' }

$.f = {
	simpleEditor:{
		lists:false,
		image:false,
		color:true,
		link:false,
		locale:'pt-BR'
	},
	advancedEditor:{
		lists:true,
		image:true,
		color:true,
		link:true,
		html:true,
		locale:'pt-BR'
	}
}

$.e = {
    buttons:'',
	navigation:'',
	spin:false,
	brand:false,
	unfollow:false,
	editorOpt:{},
	uploadOpt:uploader,
	datepickerOpt:datepick,
	w:window.innerWidth,
	h:window.innerHeight,
	lastObject:'',
	lastId:'',
	marginMax:0,
	angle:0,
	widthNow:$('html').width(),
	heightNow:$('html').height(),
	last:0,
	velocity:0,
	acceleration:50,
	holding:false,
	clicked:false,
	currentTime:CurrentTime,
	selection:false,
	price:1.19,
	option:0,
	token:'',
	objects:[],
	openedMenu:false,
	value:true, 
	marginFactor:10,
	marginTop:0,
	initial:false,
	currentYear:CurrentYear,
	position:0,
	lastVideo:'',
	videos:[],
	playerOpt:{
		width: 790, // the width of the player
		height: 430, // the height of the player
		autoPlay: true,
		showinfo: false,
		autoHide: true,
		iframed: true,
		showControls: 0,
		preferredQuality: "default",// preferred quality: default, small, medium, large, hd720
		//onPlayerEnded: play.playAgain
	}
}
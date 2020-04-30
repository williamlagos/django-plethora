$.fn.clearEvents = function(){
	$('#Canvas')
	.off('mousedown')
	.off('mouseup')
	.off('mousemove');
	
	$('.app').off('click');
	$('.pages').off('click');
	$('.login').off('click');
	$('.logout').off('click');
	$('.register').off('click');
	$('.option').off('click');
	$('.upload').off('click');
	$('.procfg').off('click');
	$('.placecfg').off('click');
	$('.controlcfg').off('click');
	$('.change').off('click');
	$('.integration,.social').off('click');
	$('.deletable').off('click');
	$('.submit').off('click');
	$('.explore').off('submit');
	$('.brand').off('click');
	$('.brand').off('hover');
	$('.participate').off('click');
	$('.next').off('click');
	$('.following').off('click');
	$('.profile').off('click');
	$('.unfollow').off('click');
	$('.unfollow').off('hover');
	$('.follow').off('click');
	$('.cancelpurchase').off('click');
	$('.deliver').off('click');
	$('.payment').off('click');
	$('.cartmore').off('click'); 
	$('.cart').off('click');
	$('.buyable').off('click');
	$('.calculate').off('click');
	$('.purchase').off('click');
	$('.pagespread').off('click');
	$('.page').off('click');
	$('.pagesave').off('click');
	$('.passwordchange').off('click');
}

$.fn.eventLoop = function () {
    $.fn.clearEvents();
	$('#Canvas')
	.on('mousedown',spin.holdHelix)
	.on('mouseup',spin.releaseHelix)
	.on('mousemove',spin.moveHelix);
	if($('.block-transparent').length) $.e.marginFactor = 0;
	else $.e.marginFactor = 10;
	
	$('a').on('click',function(){ this.blur(); });
	$('.app').on('click',$(this).showContext);
	$('.pages').on('click',$(this).showPage);
	$('.login').on('click',$.fn.authenticate);
	$('.logout').on('click',$.fn.logout);
	$('.register').on('click',$.fn.showParticipate);
	$('.option').on('click',$(this).changeOption);
	$('.upload').on('click',$.fn.input);
	$('.procfg').on('click',$.fn.submitChanges);
	$('.placecfg').on('click',$.fn.submitPlace);
	$('.controlcfg').on('click',$.fn.submitControl);
	$('.change').on('click',$.fn.doNothing);
	$('.integration,.social,.facebook,.twitter,.youtube').on('click',$(this).redirect);
	$('.deletable').on('click',$.fn.deleteObject);
	$('.submit').on('click',function(event){ $('form').tosubmit(event); });
	$('.explore').on('submit',$(this).submitSearch);
	$('.brand').on('click',$.fn.reloadMosaic);
	$('.brand').on('hover',$.fn.brandHover);
	$('.participate').on('click',$.fn.participate)
	$('.next').on('click',$.fn.nextTutorial);
	$('.following').on('click',$.fn.showFollowing);
	$('.profile').on('click',$.fn.showProfile);
	$('.unfollow').on('click',$.fn.unfollow);
	$('.unfollow').on('hover',$.fn.unfollowHover);
	$('.follow').on('click',$.fn.follow);
	$('.cancelpurchase').on('click',$.fn.cancelPurchase);
	$('.deliver').on('click',$.fn.calculateDelivery);
	$('.payment').on('click',$.fn.pay);
	$('.cartmore').on('click',$.fn.addtoBasket); 
	$('.cart').on('click',$.fn.showBasket);
	$('.buyable').on('click',$.fn.buyCoins);
	$('.calculate').on('click',$.fn.calculatePrice);
	$('.purchase').on('click',$.fn.openDeliverable);
	$('.pagespread').on('click',$.fn.submitPage);
	$('.page').on('click',$.fn.showPageEdit);
	$('.pagesave').on('click', $.fn.savePage);
	$('.passwordchange').on('click', $.fn.submitPasswordChange);
}

$.fn.mainLoop = function(){
    $.e.buttons += ' procfg imgcfg controlcfg placecfg socialcfg ';
    $.fn.eventLoop();
}
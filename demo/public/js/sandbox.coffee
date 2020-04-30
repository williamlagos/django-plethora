$(document).ready ->
  $('.page').each ->
  	$(this).html($(this).text()[2..])
  $('#Grade').showMosaic()
  $.fn.eventLoop()
      
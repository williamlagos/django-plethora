document.documentElement.style.overflowX = "hidden"

#document.documentElement.style.overflowY = 'hidden';
$(document).ready ->
  $.ajaxSetup cache: false
  $.fn.verifyProjects()
  $.fn.createPayments()
  $("#Grade").showMosaic()
  $("input:submit, button", "#botoes").button()
  $.fn.activateInterface()
  $.fn.eventLoop()
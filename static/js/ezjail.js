$(document).ready(function(){

  $(".startbutton, .stopbutton").click(function() {

    var jailname = $(this).attr('jailname');
    var action;
    if ($(this).hasClass("startbutton")) {
      action = "start";
    } else if ($(this).hasClass("stopbutton")) {
      action = "stop";
    }

    $("input[name='jailname']").val(jailname);

    var ctlform = $("#controlform");
    ctlform.attr("action", action);
    ctlform.submit();
  });

});



//-----------------------вращение иконки
$('#icon_logo').mouseenter(function () {
    $('#logo_move').addClass('fa-spin')
}).mouseleave(function(){
      $('#logo_move').removeClass('fa-spin')
    });

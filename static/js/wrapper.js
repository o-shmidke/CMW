//-----------------------вращение иконки
$('#icon_logo').mouseenter(function () {
    $('#logo_move').addClass('fa-spin')
}).mouseleave(function () {
    $('#logo_move').removeClass('fa-spin')
});


// ----------------------------------------открыть карточку пользователя
// function showHide() {
//     $('#gb_F')
//     //Если элемент с id-шником element_id существует
//     if (document.getElementById("gb_F")) {
//         //Записываем ссылку на элемент в переменную obj
//         var obj = document.getElementById("gb_F");
//         //Если css-свойство display не block, то:
//         if (obj.style.display === "block") {
//
//             obj.style.display = "none"; //Показываем элемент
//         } else obj.style.display = "block"; //Скрываем элемент
//     }
//     //Если элемент с id-шником element_id не найден, то выводим сообщение
//     else alert("Элемент с id: " + gb_F + " не найден!");
// }

// ---------------------------------------открытие формы для добавления фото
// $('#upload_photo').click('mouseclick', function (e) {
//
//     $.post('/create_photo_form/', $(this).serialize(), function (data) {
//         $('.form_photo').html(data)
//     });
//     e.preventDefault();
// });


//
// function close_form(form_upload_photo) {
//     var a = document.getElementById("form_upload_photo");
//     a.style.display = "none";
// }

$(document).mouseup(function (e) {
    var container = $("#gb_F ");
    if (container.has(e.target).length === 0) {
        container.hide();
    }
});

// $('document').ready(function () {
//
//     $('.navbarDropdown').click(function () {
//           var container = $("#gb_F ");
//     if (container.has(e.target).length === 0) {
//         container.hide();
//         container.visible
//     }
//
//
//     });
//
// });
$( document ).ready(function(){
	  // $( "#navbarDropdown" ).click(function(){ // задаем функцию при нажатиии на элемент с классом toggle
	  //   $( "#gb_F" ).toggle( "fast" ); // скрывыаем, или отображаем последний элемент <div> в документе
	  // });
	  $( "#navbarDropdown" ).click(function(){ // задаем функцию при нажатиии на элемент с классом slide-toggle
	    $( "#gb_F" ).slideToggle( "100" ); // скрывыаем, или отображаем последний элемент <div> в документе
	  });
	});
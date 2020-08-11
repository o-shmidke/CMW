//-----------------------вращение иконки
$('#icon_logo').mouseenter(function () {
    $('#logo_move').addClass('fa-spin')
}).mouseleave(function () {
    $('#logo_move').removeClass('fa-spin')
});


// ----------------------------------------открыть карточку пользователя
function showHide(gb_F) {
    //Если элемент с id-шником element_id существует
    if (document.getElementById("gb_F")) {
        //Записываем ссылку на элемент в переменную obj
        var obj = document.getElementById("gb_F");
        //Если css-свойство display не block, то:
        if (obj.style.display != "block") {
            obj.style.display = "block"; //Показываем элемент
        } else obj.style.display = "none"; //Скрываем элемент
    }
    //Если элемент с id-шником element_id не найден, то выводим сообщение
    else alert("Элемент с id: " + gb_F + " не найден!");
}

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
    if (container.has(e.target).length === 0){
        container.hide();
    }
});
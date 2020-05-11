//------------------------открытие формы добавления объекта
function showFormAdd(state) {
    document.getElementById('window').style.display = state;
    document.getElementById('gray').style.display = state;
}

//------------------------изменение цвета кнопок


let h = $('.eventBtn ');
h.bind('mousedown', function () {
    this.style.backgroundColor = '#838484';
    this.style.color = "white";
    this.style.outline = 'none';
});
h.bind('mouseup', function () {
    this.style.backgroundColor = '#5a6268';
    this.style.color = "white";
    this.style.outline = 'none';
});
h.bind('mousemove', function () {
    this.style.backgroundColor = '#5a6268';
    this.style.color = "white";
});
h.bind('mouseout', function () {
    this.style.backgroundColor = '#f5f5f5';
    this.style.color = "black";
});

// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         let cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             let cookie = jQuery.trim(cookies[i]);
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
//
// let csrftoken = getCookie('csrftoken');
//
// function csrfSafeMethod(method) {
//     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
// }
//
// $.ajaxSetup({
//     beforeSend: function (xhr, settings) {
//         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
//         }
//
//     }
// });


//-------------------------------------проверка формы на заполнение полей и запрос на сервер
$("#btn_form_add").click(function () {
    let array_str = [name_object = document.getElementById('name_object_input'),
        adress_object = document.getElementById('adress_object_input'),
        NCH_object = document.getElementById('NCH_object_input'),
        rukovoditel = document.getElementById('select_rukovoditel'),
        manager = document.getElementById('select_manager'),
        ingener = document.getElementById('select_ingener'),
        montagnik = document.getElementById('select_montagnik')];
    let errStr = document.getElementById('error');
    let sum = 0;
    for (let i = 0; i < 7; i++) {
        if (array_str[i].value === '' || typeof array_str[i] === "undefined") {
            array_str[i].style.border = '1.2px solid red';
        } else {
            array_str[i].style.border = '1px solid black';
            sum++;
        }
    }

    if (sum === 7) {
        if (!Number(array_str[2].value)) {
            array_str[2].style.border = '1.2px solid red';
            document.getElementById('error_msg').textContent = 'Значение "Н/Ч общее" должно быть числовым';
            document.getElementById('error').style.display = 'block';
        } else {
            document.getElementById('error').style.display = 'none';
            array_str[2].style.border = '1px solid black';


            $.ajax({
                type: "GET",
                url: "/add_object",
                data: {
                    'name_object_aj': $("#name_object_input").val(),
                    'adress_object_aj': $("#adress_object_input").val(),
                    'NCH_object_aj': $("#NCH_object_input").val(),
                    'rukovoditel_aj': $('#select_rukovoditel').val(),
                    'manager_aj': $('#select_manager').val(),
                    'ingener_aj': $('#select_ingener').val(),
                    'montagnik_aj': $('#select_montagnik').val(),

                },
                dataType: "text",
                cache: false,
                success: function (data) {
                    if (data === 'ok') {
                        alert("Добавлено");
                    } else if (data === 'no') {
                        alert("Ошибка");
                    }
                }
            });
        }
    } else {
        document.getElementById('error_msg').textContent = 'Необходимо заполнить все поля';
        document.getElementById('error').style.display = 'block';
    }
});



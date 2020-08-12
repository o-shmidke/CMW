
// $('#search-form').submit(function (e) {
//     $.post('/search_plan_materials/', $(this).serialize(),function (data) {
//         $('.posts').html(data)
//     });
//     e.preventDefault();
// });

// ------------------------------------------------------поиск планируемых материалов
$('#search-form_plan_materials').on('keyup input',function (e) {
    $.post('/search_plan_materials/', $(this).serialize(),function (data) {
        $('.posts').html(data)
    });
    e.preventDefault();
});

// ------------------------------------------------------поиск планируемой работы
$('#search-form_plan_works').on('keyup input',function (e) {
    $.post('/search_plan_works/', $(this).serialize(),function (data) {
        $('.posts').html(data)
    });
    e.preventDefault();
});

// ------------------------------------------------------поиск выполненой работы
$('#search-form_complete_works').on('keyup input',function (e) {
    $.post('/search_complete_works/', $(this).serialize(),function (data) {
        $('.posts').html(data)
    });
    e.preventDefault();
});




//-----------------------вращение иконки
$('#icon_logo').mouseenter(function () {
    $('#logo_move').addClass('fa-spin')
}).mouseleave(function () {
    $('#logo_move').removeClass('fa-spin')
});

// ----------------------------------------------открытие карточки пользователя
$("#navbarDropdown").click(function (e) {
        let container = $("#gb_F ");
        if (container.css("display") === "block") {
            container.slideUp(400)
        } else {
            container.slideDown(400);
        }

        e.stopPropagation();
    }
);
$('#gb_F').click(function (e) {
    e.stopPropagation();
});
$(document).click(function () {
    $('#gb_F').slideUp(400);
});



$('.errPage').ready(function () {
    $('.msgError_auth').bind('mousemove', function () {
        let start = Date.now(); // запомнить время начала
        let ic = $('.iconError_auth')

        let coordY = 50;
    let time = setInterval(frame, 10);
    function frame() {
        if (coordY === 150) {
            clearInterval(time);
        } else {
            coordY++;
            ic.style.top = coordY + 'px';
       }
    }
    });
});



$('#form_check_complete_works').on('keyup input',function (e) {
    // alert("hi");
    $.post('check_complete_works/', $(this).serialize(),function (data) {
        $('.check_nch').html(data)
    });
    e.preventDefault();
});
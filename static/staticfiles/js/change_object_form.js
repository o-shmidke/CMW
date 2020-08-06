function showFormChange(state) {
    document.getElementById('windowFormChangeObject').style.display = state;
    document.getElementById('grayFormChangeObject').style.display = state;
}


$("#select_object").on("change", function () {
    let id_objectValue = $("#select_object").val()


    // $.ajax({
    //     //     type: "GET",
    //     //     url: "/form_change_object_view",
    //     //     data: {
    //     //         'id_object_aj': id_objectValue
    //     //     },
    //     //     dataType: "json",
    //     //     cache: false,
    //     //     success: function (result) {
    //     //         // if (data === 'ok') {
    //     //         //     alert(data);
    //     //         // } else if (data === 'no') {
    //     //         //     alert("Ошибка");
    //     //         // }
    //     //         alert(result.context);
    //     //     }
    //     // });
})
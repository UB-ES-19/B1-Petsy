function sendRegister() {
    var form = $("#edit_profile_form");

    $.ajax({
        url: '/edit_profile/',
        data: form.serialize(),
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if(data.response_code==200){
                location.reload()
            }
            if(data.response_code==204){
                location.reload()
            }
        }
    });
}
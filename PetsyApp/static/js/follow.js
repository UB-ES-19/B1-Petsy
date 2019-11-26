function follow(id_user, csrf_token, btn, contador) {
    $.ajax({
        url: '/follow/',
        data: {
            "csrfmiddlewaretoken": csrf_token,
            "following": id_user
        },
        type:'POST',
        dataType: 'json',
        success: function (data) {
            if (data.response_code == 200) {
                var num = Number(contador.innerText) - 1;
                contador.innerText = num + "";
                btn.innerText = "Seguir usuario";
            }
            else if (data.response_code == 201) {
                var num = Number(contador.innerText) + 1;
                contador.innerText = num + "";
                btn.innerText = "Dejar de seguir";
            }
            else if (data.response_code == 400) {
                alert(data.response_msg);
                location.reload();
            }
        }
    });
}
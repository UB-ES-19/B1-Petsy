function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function validaLogin() {
    if($("#email_login").val() == ""){
        alert("El campo Email no puede estar vacío.");
        $("#email_login").focus();       // Esta función coloca el foco de escritura del usuario en el campo Nombre directamente.
        return false;
    }
    if($("#password_login").val() == ""){
        alert("El campo Password no puede estar vacío.");
        $("#password_login").focus();       // Esta función coloca el foco de escritura del usuario en el campo Nombre directamente.
        return false;
    }
    console.log("OK")
    return true;
}

function sendLogin(e) {
    e.preventDefault();
    var form = $("#my-form-login");
    $.ajax({
        url: '/login/',
        data: form.serialize(),
        dataType: 'json',
        success: function (data) {
            if (data.login_successful) {
                alert("Login successful");
                $('#registro').modal('toggle');
            } else {
                var error_msg = "Login unsuccessful due to the following reason\n";
                if (data.response_code == 404) {
                    error_msg += "User doesn't exist";
                    $("#email_login").value = "";
                } else if (data.response_code == 403) {
                    error_msg += "Wrong password";
                    $("#password_login").value = "";
                }
                alert(error_msg);
            }
        }
    });
}

function validaRegister() {
    if($("#email").val() == ""){
        alert("El campo Email no puede estar vacío.");
        $("#email").focus();       // Esta función coloca el foco de escritura del usuario en el campo Nombre directamente.
        return false;
    }
    if($("#username").val() == ""){
        alert("El campo Username no puede estar vacío.");
        $("#username").focus();       // Esta función coloca el foco de escritura del usuario en el campo Nombre directamente.
        return false;
    }
    if($("#password").val() == ""){
        alert("El campo Password no puede estar vacío.");
        $("#password").focus();       // Esta función coloca el foco de escritura del usuario en el campo Nombre directamente.
        return false;
    }
    if(checkPassword()){
        return true;
    }

    return false;
}

function sendRegister(e) {
    e.preventDefault();
    var form = $("#my-form-register");
    $.ajax({
        url: '/register/',
        data: form.serialize(),
        dataType: 'json',
        success: function (data) {
            if (data.login_successful) {
                alert("Login successful");
            } else {
                var error_msg = "Login unsuccessful due to the following reason\n";
                if (data.response_code == 404) {
                    error_msg += "User doesn't exist";
                } else if (data.response_code == 403) {
                    error_msg += "Wrong password";
                }
                alert(error_msg);
            }
        }
    });
}

function checkPassword() {
        var pass1 = document.getElementById("password");
        var bol = false;
        if (pass1.value.length>=8){
            bol = true;
        }
        if (bol){
            return true;
        }
        return false;
}
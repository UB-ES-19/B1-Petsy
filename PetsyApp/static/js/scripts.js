$("#login_form").submit(function (e) {
    e.preventDefault();
    if (validaLogin()) {
        sendLogin();
    }
});

$("#register_form").submit(function (e) {
    e.preventDefault();
    if(validaRegister()){
        sendRegister();
    }
});

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
    return true;
}

function sendLogin() {
    var form = $("#login_form");
    $.ajax({
        url: "/login/",
        data: form.serialize(),
        type:'POST',
        dataType: 'json',
        success: function (data) {
            if (data.login_successful) {
                alert("Login successful");
                location.reload();
            } else {
                //var error_msg = "Login unsuccessful due to the following reason\n";
                var error_msg = "";
                if (data.response_code == 404) {
                    error_msg += "User doesn't exist";
                    $('#test').append(error_msg);
                    $("#email_login").val('');
                    $("#password_login").val('');
                } else if (data.response_code == 403) {
                    error_msg += "Wrong password";
                    $('#test').append(error_msg);
                    $("#password_login").val('');
                }
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

function sendRegister() {
    var form = $("#form_register");
    $.ajax({
        url: '/register/',
        data: form.serialize(),
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.login_successful) {
                alert("Register successful");
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
"use strict";

//login form event handler -- secure if SSL
function validateUser(evt) {
    evt.preventDefault();
    
    // var loginInfo = $("#login").serialize();

    $.post('signin/', $("#login").serialize(), function(result) {

        if (result === "Fail") {
            $('#login-fail').html("Incorrect username or password");
        } else {
            $('#LoginModal').modal('hide');
            $('#loginNav').attr('src', 'signout/').html('Log Out');
        }
    })
}

//login form event binding
$('#login').on('submit', validateUser);



     $("#confirmPass").keyup(checkPass);

    function checkPass() {
        var password = $("#password").val();
        var confirmPassword = $("#confirmPass").val();

        if (password !== confirmPassword) {

            $("#divCheckPass").html("Passwords do not match!");
            return 1;
        } else {

            $("#divCheckPass").html("");
            return 0;
        }
    }

    //$(document).ready(function () {
    //    $("#confirmPass").keyup(checkPass);
    //});

    $('#signUpBtn').on("click", function (event) {
        event.preventDefault();
        console.log("success in Register button press");

        var email = $('#email').val();
        var user = $('#username').val();
        var pass = $('#password').val();
        var confirmPass = $('#confirmPass').val();


        if (checkPass() === 1) {
            $.ajax({
                url: '/Register',
                data: $('form').serialize(),
                type: 'POST',
                success: function (response) {
                    var obj = JSON.parse(response);
                    if (obj.status === 'OK') {
                        $("#username").val("");
                        $("#password").val("");
                        $("#confirmPass").val("");
                        $("#email").val("");
                        console.log(response);

                        //Scripts for determining type of user and type of screen redirect
                        //default is Visitor Homepage until future commit

                        setTimeout(openVisitorHomepage, 3000);
                    }
                    else {
                        $("#password").val("");
                        var errorMessage = ''
                        var errorResponses = ["Should be at least 8 characters in length. "
                            , "Should have at least 1 uppercase character. ", "Should have at least 1 number. "];
                        var UserNotFound = "User not found in database";

                        obj.pass.forEach(function (e_m) {
                            errorMessage += errorResponses[e_m];
                        });
                        $("#invalid-pass").removeAttr('hidden')
                            .text(user + ", the password or user login data is invalid: " + errorMessage
                                + "Or " + UserNotFound + ", Please try again");
                    }
                },
                error: function (error) {
                    console.log(error);
                }
            });
        } else {
            console.log("error passwords do not match for Register");
        }
    });


function openVisitorHomepage(){
    window.location.href = "/visitorHomePage";
}

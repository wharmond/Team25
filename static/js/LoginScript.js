$(function(){

	   $('#Login_btn').on("click", function(event){
           event.preventDefault();
           console.log("success in Login button press");

            var user = $('#inputUsername').val();
            var pass = $('#inputPassword').val();
            $.ajax({
                url: '/signIn',
                data: $('form').serialize(),
                type: 'POST',
                success: function(response) {
                        var obj = JSON.parse(response);
                        if (obj.status === 'OK') {
                            $("#inputUsername").val("");
                            $("#inputPassword").val("");
                            console.log(response);

                            //Scripts for determining type of user and type of screen redirect
                            //default is Visitor Homepage until future commit

                            setTimeout(openVisitorHomepage, 3000);
                        }
                        else{
                            $("#inputPassword").val("");
                            var errorMessage = ''
                            var errorResponses = ["Should be at least 8 characters in length. "
                                ,"Should have at least 1 uppercase character. ","Should have at least 1 number. "];
                            var UserNotFound = "User not found in database";

                            obj.pass.forEach(function(e_m){
                                errorMessage += errorResponses[e_m];
                            });
                            $("#invalid-pass").removeAttr('hidden')
                                              .text(user + ", the password or user login data is invalid: " + errorMessage
                                                  + "Or " + UserNotFound + ", Please try again");
                            }
                },
                error: function(error){
                    console.log(error);
                }
            });
	    });

	   $('#Register_btn').click(function() {

            console.log("success in Registration button press");
            window.location.href = "/Register";
	   });
});

function openVisitorHomepage(){
    window.location.href = "/visitorHomePage";
}

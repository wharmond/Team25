$(function(){
	$('button').click(function(){
        var user = $('#inputUsername').val();
		var pass = $('#inputPassword').val();
		$.ajax({
			url: '/signUpUser',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response) {
                    var obj = JSON.parse(response);
                    if (obj.status === 'OK') {
                        $("#invalid-pass").text("");
                        $("#valid-pass").removeAttr('hidden')
                                        .text("Congratulations on registering for CSE6242, " + user + ". Redirecting you to the course homepage...");
                        $("#inputUsername").val("");
                        $("#inputPassword").val("");
                        console.log(response);
                        setTimeout(openPopup, 3000);
                    }
                    else{
                        $("#inputPassword").val("");
                        var errorMessage = ''
                        var errorResponses = ["Should be at least 8 characters in length. ","Should have at least 1 uppercase character. ","Should have at least 1 number. "];
                        obj.pass.forEach(function(e_m){
                            errorMessage += errorResponses[e_m];
                        });
                        $("#invalid-pass").removeAttr('hidden')
                                          .text(user + ", the password is invalid: " + errorMessage + " Please try again");
                        }
            },
			error: function(error){
				console.log(error);
			}
		});
	});
});

function openPopup(){
    window.location.href = "http://poloclub.gatech.edu/cse6242/";
}
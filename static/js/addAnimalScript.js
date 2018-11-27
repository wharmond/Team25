function addAnimalSubmit() {

    var exhibit = $('#exhibit').val();
    var animalName = $('#animalName').val();
    var species = $('#species').val();
    var age = $('#age').val();
    var animalType = $('#animalType').val();

    url: '/Register',
    data: $('form').serialize(),
    type: 'POST',
    success: function (response) {
        var obj = JSON.parse(response);
        if (obj.status === 'OK') {
            $("#animalName").val("");
            $("#species").val("");
            $("#age").val("");
            $("#exhibit").val("");
            $("#animalType").val("");
            console.log(response);

            //Scripts for determining type of user and type of screen redirect
            //default is Visitor Homepage until future commit
            alert("Success! " + animalName + " has been added to the database.");
            setTimeout(openAdminViewAnimals, 2000);
        }
        else {
           alert("Error! Please check your inputs.")
        }
    },
    error: function (error) {
        console.log(error);
    }
});
        } else {
            $("#divCheckPass").html("Passwords do not match!");
        }
  }

function openAdminViewAnimals() {
    window.location.href = "/addAnimal";
}
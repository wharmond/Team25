$(function(){
    $('button').click(function() {
        $('#search_exhibits_btn').click(function(){
           console.log("success in search exhibit button press");
           window.location.href = "/searchExhibits";
        });

        $('#view_exhibit-history').click(function() {
            console.log("success in view exhibit history button press");
            window.location.href = "/viewExhibitHistory";
        });

        $('#view_shows').click(function() {
            console.log("success in view shows  button press");
            window.location.href = "/viewShows";
        });

        $('#view_show_history').click(function() {
            console.log("success in view show history button press");
            window.location.href = "/viewShowHistory";
        });

        $('#search_for_animals').click(function() {
            console.log("success in search for animals button press");
            window.location.href = "/SearchAnimals";
        });

        $('#log_out').click(function() {
            console.log("success in log out button press");
            window.location.href = "/SearchAnimals";
        });

    });
});

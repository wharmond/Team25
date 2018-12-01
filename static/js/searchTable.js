function searchTable() {
    var showName, showExhibit, showDate, table, tr;
    showName = document.getElementById("showName").value;
    showExhibit = document.getElementById("showExhibit").value;
    showDate = document.getElementById("showDate").value;
    table = document.getElementById("showsTable");
    tr = table.getElementsByTagName("tr");

    // Check if inputs have values and run appropriate script
    if (showName != "") {
        nameFilter(showName, tr);
    }
    if (showExhibit != "") {
        nameFilter(showExhibit, tr);
    }
}

function nameFilter(input, tr) {
    // Declare variables
    var td, i, txtValue;
    filter = input.toUpperCase();

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}
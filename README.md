# Team25
CS 4400 Project


The website will have the following pages:  
  /Home  
    - Contains list of shows within the next week  
    - Links to Animals, Login, and Exhibits  
  /Login  
    - Allows users to login or register a new account  
      * doing this on the same page because there's no need making it needlessly complex  
    - If a user already exists or a password is not valid, an error message will appear on the screen.  
      * "Error: <errors>"  
    -> Successful login take the user to the homepage corresponding to the user type  
  /User  
    - There are 3 user types which will have different displys  
      1. /Visitor  
        - Displays their previously visited shows and exhibits  
      2. /Staff/  
        - Displays any shows the staff member hosts  
        - Displays any notes recently created by staff member  
        - Link to create new note  
      3. /Admin/  
        - Displays any recently created notes  
        - Link to create new note  
        - Form to add/drop users  
        - Form to add/drop animals  
  /Notes  
    - List of all notes  
    - Form to create new note  
  /Exhibits  
    - Lists exhibit information  
      - Open/Close information (?)  
      - Shows hosted in exhibit  
      - Animals in exhibit  
  /Shows  
    - Show information  
      - Show start time  
      - Animals in show  
      - Location  
      - Host(s)  

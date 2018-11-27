# Team25
## CS 4400 Project


### Pages:  
####  /Home  
    - Determine user type
    - Option to either log in or register
    - Contains list of shows within the next week (this is only visible once you login in to database)
    - Links to Animals, Login, and Exhibits (this is only visible once you login in to database)
#### /Registration
    - Enter email (must be unique and valid)
    - Enter username (must be unique)
    - Enter password (must be at least 8 characters)
    - Confirm password (must match the above password)
####  /Login  
    - Allows users to login or register a new account  
      * doing this on the same page because there's no need making it needlessly complex  
    - If a user already exists or a password is not valid, an error message will appear on the screen.  
      * "Error: <errors>"  
      * Password must be at least 8 characters long and then has to be hashed
      * must ensure that the email has an @ and a .
    -> Successful login take the user to the homepage corresponding to the user type  
####  /User  
    - There are 3 user types which will have different displys  
      1. /Visitor  
        - Search Exhibits
        - Search Shows
        - View Exhibit History
        - View Show History
        - Search animals
        - Log out
      2. /Staff/  
        - Displays any shows the staff member hosts (not on staff home page; this after you push view show button)
            - Table - name, time (day and time) exhibit
        - Displays any notes recently created by staff member (not on staff home page) - i dont know how exactly you get to this page
        - Link to create new note  (not on staff home page)
        - Search Animals button
        - View Shows button
        - Logout button
      3. /Admin/  
        - Displays any recently created notes (not on admin home page)
        - Link to create new note  (not on admin home page) 
        - Form to add/drop users (not on admin home page) 
        - Form to add/drop animals (not on admin home page)
        - View visitors button
        - View Staff button
        - View Shows button
        - View Animals button
        - Add Animals button
        - Add Show button
####  /Notes  
    - List of all notes  
    - Form to create new note
####  /Exhibits  
    - Lists exhibit information
      - Open/Close information (?)  
      - Shows hosted in exhibit (this is not shown in exhibit detail)
      - Animals in exhibit (this is shown in table as listed below)
      - Name, size, num animals, and water feature on one line
      - button option to log vidit
      - Table with name and species in exhibit
####  /Shows  
    - Show information  
      - Show start time  
      - Animals in show  
      - Location  
      - Host(s)  
#### /Search Exhibits
    - Name
    - Number of animals (with min and max)
    - Size (with min and max)
    - Water feature (boolean - yes or no)
    - Search button
    - Table - name, size, numanimals, water (at bottom)
#### /Animal
    - Name
    - Species
    - Age (in months)
    - Exhibit name
    - type (mammal, bird, amphibian, reptile, fish, or invertebrate)
#### /Search Animals
    - Exhibit
    - Name
    - Age (with min and max)
    - Species
    - Type (drop down with above choices)
    - Search button
    - Table - name, speciies, exhibit, age, type (at bottom)
#### /Search Shows
    - Name
    - Date (with calendar option)
    - Exhibit (drop down)
    - Search button
    - Table - name, exhibit, date (day and time) (at bottom)
    - Option to log visit by pushing button
#### /Exhibit History
    - Name
    - Number of Visits (with min and max)
    - Time (with calendar option)
    - Search button
    - Table - name, time (day and time), number of visits (at bottom)
#### /Show History
    - Name
    - Exhibit (with drop down)
    - Time (with calendar option)
    - Search button
    - Table - name, time (day and time), exhibit (at bottom)
#### /Animal Care
    - Name, species, age, exhibit, type all already entrered
    - text box for notes
    - button to log notes
    - Table - staff member, note, time (day and time) (at bottom)
#### /View Visitors
    - Table - username, email
    - Delete Visitor button
#### /View Staff
    - Table - username, email
    - Delete Staff Member button
#### /View Shows
    - Name
    - Date (calendar option)
    - Exhibit
    - Search button
    - Table - name, exhibit, date (day and time) (at bottom)
    - Remove Show button
#### /View Animals
    - Exhibit (drop down menu)
    - Name
    - Age (with min and max)
    - Species
    - Type (with drop down menu)
    - Search button
    - Table - name, species, exhibit, age, type (at bottom)
    - Remove Animal Button
#### /Add Animal
    - Name
    - Exhibit (drop down)
    - Type (drop down)
    - Species
    - Age (integer drop down)
    - Add Animal button
#### / Add Shows
    - Name
    - Exhibit (drop down)
    - Staff (drop down)
    - Date (calendar option)
    - Time
    - Add Show button

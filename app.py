from flask import Flask, render_template, request, json, session
import pymysql, re
import hashlib

app = Flask(__name__)
# Secret key for secure user sessions
app.secret_key = "Secret_Key"


class Database:
    # The socket SQL server is running on your computer (locally)
    host = "127.0.0.1"
    user = "root"
    # SQL Server password
    password = "password"
    # the Database Schema name
    db = "AtlantaZoo"
    charSet = "utf8mb4"

    # Create the connection with configured parameters, autocommit specifies whether SQL INSERT statements actually
    # insert, leave to false if you just want to test if an INSERT query executes correctly
    con = pymysql.connect(host=host, user=user, password=password, autocommit=True, db=db, charset=charSet,
                          cursorclass=pymysql.cursors.DictCursor)

    # Obtain a cursor for executing queries
    cur = con.cursor()

    # Execute this query if you don't want to setup the local SQL server tables
    sqlQuery = ("CREATE TABLE Users(\n"
                "            Username VARCHAR(50) NOT NULL UNIQUE,\n"
                "            Password VARCHAR(255) NOT NULL,\n"
                "            Email VARCHAR(50) NOT NULL UNIQUE,\n"
                "            UserType VARCHAR(50) NOT NULL, \n"
                "            PRIMARY KEY(Username),\n"
                "            CHECK(Email LIKE ‘%@%.%’)\n"
                "        );\n"
                "            \n"
                "        CREATE TABLE Admins(\n"
                "            Username VARCHAR(50) NOT NULL,\n"
                "            PRIMARY KEY(Username),\n"
                "            FOREIGN KEY(Username)REFERENCES Users(Username) ON UPDATE CASCADE ON DELETE CASCADE\n"
                "        );\n"
                "        \n"
                "        CREATE TABLE Staff(\n"
                "            Username VARCHAR(50) NOT NULL,\n"
                "            PRIMARY KEY(Username),\n"
                "            FOREIGN KEY(Username)REFERENCES Users(Username) ON UPDATE CASCADE ON DELETE CASCADE\n"
                "        );\n"
                "        \n"
                "        CREATE TABLE Visitor(\n"
                "            Username VARCHAR(50) NOT NULL,\n"
                "            PRIMARY KEY(Username),\n"
                "            FOREIGN KEY(Username)REFERENCES Users(Username) ON UPDATE CASCADE ON DELETE CASCADE\n"
                "        );\n"
                "        \n"
                "        CREATE TABLE Exhibits(\n"
                "            ExhibitName VARCHAR(50) NOT NULL UNIQUE,\n"
                "            WaterFeature BOOLEAN,\n"
                "            Size INTEGER,\n"
                "            PRIMARY KEY(ExhibitName)\n"
                "        );\n"
                "        \n"
                "        CREATE TABLE Animals(\n"
                "            AnimalName VARCHAR(50) NOT NULL,\n"
                "            Species VARCHAR(50) NOT NULL,\n"
                "            Exhibit VARCHAR(50),\n"
                "            Age INTEGER,\n"
                "            Type_of_Animal VARCHAR(50),\n"
                "            PRIMARY KEY(AnimalName, Species),\n"
                "            FOREIGN KEY(Exhibit)REFERENCES Exhibits(ExhibitName) ON UPDATE CASCADE ON DELETE RESTRICT\n"
                "        );    \n"
                "        \n"
                "        CREATE TABLE Shows(\n"
                "            ShowName VARCHAR(100) NOT NULL,\n"
                "            Date_Time DATETIME NOT NULL,\n"
                "            LocatedAt VARCHAR(50) NOT NULL,\n"
                "            HostedBy VARCHAR(50) NOT NULL,\n"
                "            PRIMARY KEY(ShowName, Date_Time),\n"
                "            FOREIGN KEY(LocatedAt)REFERENCES Exhibits(ExhibitName) ON UPDATE CASCADE ON DELETE RESTRICT,\n"
                "            FOREIGN KEY(HostedBy)REFERENCES Staff(username) ON UPDATE CASCADE ON DELETE CASCADE\n"
                "        );    \n"
                "            \n"
                "        CREATE TABLE ShowVisits(\n"
                "            ShowName VARCHAR(100) NOT NULL,\n"
                "            Date_Time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,\n"
                "            Visitor VARCHAR(50) NOT NULL,\n"
                "            PRIMARY KEY(ShowName, Date_Time, Visitor),\n"
                "            FOREIGN KEY(ShowName, Date_Time)REFERENCES Shows(ShowName, Date_Time) ON UPDATE CASCADE ON DELETE CASCADE,\n"
                "            FOREIGN KEY(Visitor)REFERENCES Visitor(username) ON UPDATE CASCADE ON DELETE CASCADE\n"
                "        );\n"
                "            \n"
                "        CREATE TABLE ExhibitVisits(\n"
                "            Visitor VARCHAR(50) NOT NULL,\n"
                "            ExhibitName VARCHAR(50) NOT NULL,\n"
                "            Date_Time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,\n"
                "            PRIMARY KEY(Visitor, ExhibitName, Date_Time),\n"
                "            FOREIGN KEY(Visitor)REFERENCES Visitor(Username) ON UPDATE CASCADE ON DELETE CASCADE,\n"
                "            FOREIGN KEY(ExhibitName)REFERENCES Exhibits(ExhibitName) ON UPDATE CASCADE ON DELETE RESTRICT\n"
                "        );\n"
                "        \n"
                "        CREATE TABLE Notes(\n"
                "             Staff VARCHAR(50) NOT NULL,\n"
                "             Date_Time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,\n"
                "             Text_Input VARCHAR(250),\n"
                "             AnimalName VARCHAR(50) NOT NULL,\n"
                "             Species VARCHAR(50) NOT NULL,\n"
                "             PRIMARY KEY(Staff, Date_Time, AnimalName, Species),\n"
                "             FOREIGN KEY(Staff)REFERENCES Staff(Username) ON UPDATE CASCADE ON DELETE CASCADE,\n"
                "             FOREIGN KEY(AnimalName, Species)REFERENCES Animals(AnimalName, Species) ON UPDATE CASCADE ON DELETE CASCADE\n"
                "        );\n"
                "        ")

    #
    # Create Initial Users SQL Query, execute this if you want to run SQL server with this schema data
    #

    create_users = """Insert into Users values ("martha_johnson","password1",	"marthajohnson@hotmail.com", "staff");
                        Insert into Users values ("ethan_roswell","password3",	"ethanroswell@yahoo.com", "staff");                    
                        Insert into Users values ("xavier_swenson","password4",	"xavierswenson@outlook.com", "visitor");                        
                        Insert into Users values ("isabella_rodriguez","password5",	"isabellarodriguez@mail.com", "visitor");                        
                        Insert into Users values ("nadias_tevens","password6",	"nadiastevens@gmail.com", "visitor");                
                        Insert into Users values ("robert_bernheardt","password7",	"robertbernheardt@yahoo.com", "visitor");                  
                        Insert into Users values ("admin1","adminpassword",	"adminemail@mail.com", "admin");
                        """

    #
    # Create Exhibits SQL Query, execute this if you want to run SQL server with this schema data w/o manually doing it
    #
    create_exhibits = ('INSERT into Exhibits values("Pacific", 1, 850);\n'
                       '                        INSERT into Exhibits values("Jungle", 0, 600);\n'
                       '                        INSERT into Exhibits values("Sahara", 0, 1000);\n'
                       '                        INSERT into Exhibits values("Mountainous", 0, 1200);\n'
                       '                        INSERT into Exhibits values("Birds", 1, 1000);')

    #
    # Create Animals SQL Query, execute if your preference is to avoid setting up the server manually
    #

    create_animals = """Insert into Animals values ("Goldy", "Goldfish" , "Pacific", 2, "Fish");                        
                        Insert into Animals values ("Nemo", "Clownfish" , "Pacific", 2, "Fish");                        
                        Insert into Animals values ("Pedro", "Poison Dart frog" , "Jungle", 3, "Amphibian");                        
                        Insert into Animals values ("Lincoln", "Lion" , "Sahara", 8, "Mammal");                        
                        Insert into Animals values ("Greg", "Goat" , "Mountainous", 6, "Mammal");                        
                        Insert into Animals values ("Brad", "Bald Eagle" , "Birds", 4, "Bird");"""

    #
    # Populate Visitor table
    #
    create_visitor = """INSERT into Visitor
                        values("xavier_swenson");                    
                        INSERT into Visitor
                        values("isabella_rodriguez");                        
                        INSERT into Visitor
                        values("nadias_tevens");                        
                        INSERT into Visitor
                        values("robert_bernheardt");                      
                        """

    #
    # Populate Staff table needed for the Shows table "hosted_by" foreign key, must execute above queries in order to work
    #

    create_staff = """Insert into Staff values("martha_johnson");
                        Insert into Staff values("benjamin_rao");
                        Insert into Staff values("ethan_roswell");"""

    #
    # Populate Admin table
    #
    create_admin = """Insert into Admins values("admin1");"""

    #
    # Create Shows with foreign key "hosted_by" referencing staff table
    #

    create_shows = """INSERT into Shows
                        values("Jungle Cruise", "2018-10-06 09:00:00", "Jungle", "martha_johnson");                       
                        INSERT into Shows
                        values("Feed the Fish", "2018-10-08 12:00:00", "Pacific", "martha_johnson");                       
                        INSERT into Shows
                        values("Fun Facts", "2018-10-09 15:00:00", "Sahara", "martha_johnson");                       
                        INSERT into Shows
                        values("Climbing", "2018-10-10 16:00:00", "Mountainous", "benjamin_rao");                        
                        INSERT into Shows
                        values("Flight of the Birds", "2018-10-11 15:00:00", "Birds", "ethan_roswell");                        
                        INSERT into Shows
                        values("Jungle Cruise", "2018-10-12 14:00:00", "Jungle", "martha_johnson");                        
                        INSERT into Shows
                        values("Feed the Fish", "2018-10-12 14:00:00", "Pacific", "ethan_roswell");                       
                        INSERT into Shows
                        values("Fun Facts", "2018-10-13 13:00:00", "Sahara", "benjamin_rao");                       
                        INSERT into Shows
                        values("Climbing", "2018-10-13 17:00:00", "Mountainous", "benjamin_rao");                        
                       INSERT into Shows
                        values("Flight of the Birds", "2018-10-14 14:00:00", "Birds", "ethan_roswell");                       
                        INSERT into Shows
                        values("Bald Eagle", "2018-10-15 14:00:00", "Birds", "ethan_roswell");
                        """

    # # # # # # # # # # # # SQL Scripts Below (called by syntax: "Database.{class_method_name}  # # # # # # # # # # # #
    #
    #
    # # # # # # # # # # # # SQL Scripts for Login/Registration and Validation # # # # # # # # # # # #
    #
    #

    @classmethod
    def login(cls, email, user_pass):
        print("login: email: " + email + ", pass: " + user_pass)

        # Query matches email field and password to Users table in database, returns boolean 0 if not found, 1 otherwise
        login_query = "SELECT * FROM Users WHERE Users.Email = %s AND Users.Password = %s"
        result = cls.cur.execute(login_query, (email, user_pass))
        print("Query returned: " + str(result))

        return result

    @classmethod
    def get_userType(cls, email):
        userType_query = ("Select UserType FROM Users WHERE Users.Email = %s")
        cls.cur.execute(userType_query, email)
        result = cls.cur.fetchone()
        print("User type returned: " + str(result))
        return result['UserType']

    @classmethod
    def register(cls, username, password, email, user_type):
        """
            Returns 0 if the SQL INSERT Operation fails, returns a non-zero value otherwise (INSERT successful)
        :param username:
        :param password:
        :param email:
        :param user_type:
        :return: 0 if INSERT fails, > 0 otherwise
        """
        print("register query provided parameters: " + username + ',' + password + "," + email + "," + user_type)

        Register_query = "Insert into Users values (%s, %s, %s, %s)"
        try:
            result = cls.cur.execute(Register_query, (username, password, email, user_type))

            print("Register Query returned: " + str(result))

            return result

        except Exception as e:
            print("Exeception occured:{}".format(e))
        finally:
            return 0

    @classmethod
    def showTables(cls):
        cls.cur.execute("show tables")
        rows = cls.cur.fetchall()
        for row in rows:
            print(row)

    #
    #
    # # # # # # # # # # # # SQL Scripts for Visitor # # # # # # # # # # # #
    #
    #

    @classmethod
    def searchExhibits(cls):
        """
        Query that gets all Exhibits available and animal count in the exhibit
        :return:
        """
        Search_query = "SELECT Distinct e.ExhibitName, e.WaterFeature, e.Size, count(a.Exhibit = e.ExhibitName ) " \
                       "as NumAnimals FROM Exhibits as e left join Animals as a on a.Exhibit = e.ExhibitName " \
                       "group by e.Size, e.ExhibitName, e.WaterFeature"
        cls.cur.execute(Search_query)
        result = cls.cur.fetchall()
        print("Search Exhibits result: " + str(result))
        return result

    @classmethod
    def search_for_animals(cls):
        search_animals_query = (
            "SELECT DISTINCT a.AnimalName as Name, a.Species, a.Exhibit, a.Age, a.Type_of_Animal  \n"
            " as Type FROM Animals as a G"
            "ROUP BY a.AnimalName, a.Species, a.Exhibit, a.Age, a.Type_of_Animal")
        cls.cur.execute(search_animals_query)
        result = cls.cur.fetchall()
        print("Search for animals result: " + str(result))
        return result

    @classmethod
    def view_exhibit_history(cls):
        exhibit_history_query = (
            "SELECT DISTINCT a.AnimalName as Name, a.Species, a.Exhibit, a.Age, a.Type_of_Animal  \n"
            " as Type FROM Animals as a G"
            "ROUP BY a.AnimalName, a.Species, a.Exhibit, a.Age, a.Type_of_Animal")
        cls.cur.execute(exhibit_history_query)
        result = cls.cur.fetchall()
        print("Search for animals result: " + str(result))
        return result

    #
    #
    # # # # # # # # # # # # SQL Scripts for Admin # # # # # # # # # # # #
    #
    #

    @classmethod
    def add_animals(cls, animal_name, species, exhibit, age):
        add_animal_query = "Insert into Users values (%s, %s, %s, %s)"

        cls.cur.execute(add_animal_query)
        try:
            result = cls.cur.execute(add_animal_query, (animal_name, species, exhibit, age))

            print("Add Animal Query returned: " + str(result))

            return result

        except Exception as e:
            print("Exeception occured:{}".format(e))
        finally:
            return 0
        searchResult = cls.cur.fetchall()
        print("Animal Search result: " + str(searchResult))


#
#
# # # # # # # # # # # # Login/Registration Pages & Validation Server Scripts Below # # # # # # # # # # # #
#
#


@app.route("/")
def login():
    return render_template('Login.html')


@app.route("/signIn", methods=['POST'])
def signIn():
    user = request.form['username']
    password = request.form['password']

    if isValidPassword(password):
        Database.showTables()
        result = Database.login(user, password)

        if result is not 0:
            # If user exists in database, find corresponding user type
            print("query returned valid username")
            session['email'] = user
            session['user_type'] = Database.get_userType(user)
            print("session user_type is: " + session['user_type'])
            return json.dumps({'status': 'OK', 'user': user, 'user_type': session['user_type']})
        else:
            print("User not found in resulted query")
            return json.dumps({'status': 'BAD', 'user': user, 'pass': 'error'})
    else:
        print("Error in login, invalid login data")
        return json.dumps({'status': 'BAD', 'user': user, 'pass': 'error'})


@app.route('/RegisterScreen')
def RegisterScreen():
    return render_template("Registration.html")


@app.route('/Register', methods=['POST'])
def Register():
    print("Register POST request received")
    email = request.form['email']
    # session['username'] = user
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password']

    # Conditional Statement checks if email, password and confirmPass are all correct and that the user does not exist
    # already in the database
    if isValidEmail(email) and isValidPassword(password) and (password == password2) and (
            Database.login(email, password) is 0):
        print("valid email & pass provided: " + email + ", " + password)

        # Check if Staff checkbox is checked
        if request.form.get('user-type'):
            print("Staff checkbox in Registration page checked")
            visitor_userType = "staff"
        else:
            print("Staff checkbox in Registration page NOT checked")
            visitor_userType = "visitor"

        result = Database.register(username, password, email, visitor_userType)

        if result is not 0:
            print("returning valid json with status OK and setting current user session username and type")
            session['email'] = email
            session['user_type'] = Database.get_userType(email)
            return json.dumps({'status': 'OK', 'email': email, 'user_type': session['user_type']})
        else:
            print("returning json with status BAD")
            return json.dumps({'status': 'BAD', 'email': email, 'pass': 'error'})

    else:
        print("Invalid email or password input provided or User Exists in database: " + email + ", pass: " + password)
        return json.dumps({'status': 'BAD', 'email': email, 'pass': 'error', 'error': 'User_Exists'})


@app.route("/addNote")
def addNote():
    return json.dumps({'status': 'OK', 'note': "note"})


#
#
# # # # # # # # # Visitor, Staff, Admin HomePages # # # # # # # # #
#
#


@app.route('/visitorHomePage')
def visitor_homepage():
    return render_template("./VisitorTemplates/Visitor_Homepage.html")


@app.route('/staffHomePage')
def staff_homepage():
    return render_template("./StaffTemplates/staff_Homepage.html")


@app.route('/adminHomePage')
def admin_homepage():
    return render_template("./AdminTemplates/Admin_Homepage.html")


#
#
# # # # # # Visitor Pages (excluding /LogOut) # # # # # #
#
#


@app.route('/searchExhibits')
def search_exhibits():
    rows = Database.searchExhibits()
    # pass returned SQL query into jinja HTML template
    return render_template("./VisitorTemplates/SearchExhibits.html", rows=rows)


@app.route('/viewExhibitHistory')
def view_exhibit_history():
    return render_template("./VisitorTemplates/ExhibitHistory.html")


@app.route('/viewShows')
def view_shows():
    return render_template("TestPage.html")


@app.route('/viewShowHistory')
def view_show_history():
    return render_template("TestPage.html")


@app.route('/SearchForAnimals')
def search_for_animals():
    rows = Database.search_for_animals()
    # pass returned SQL query into jinkja HTML template
    return render_template("./VisitorTemplates/searchAnimals.html", rows=rows)


#
#
# # # # # # Staff Pages (excluding /LogOut) # # # # # #
#
#

@app.route('/StaffSearchAnimals')
def search_animals():
    return render_template("TestPage.html")


@app.route('/StaffViewShows')
def staff_view_shows():
    return render_template("TestPage.html")


#
#
# # # # # # # # Admin Pages Below (excluding /LogOut) # # # # # # # #
#
#


@app.route('/viewVisitors')
def view_visitors():
    return render_template("TestPage.html")


@app.route('/viewStaff')
def view_staff():
    return render_template("TestPage.html")


@app.route('/AdminViewShows')
def admin_view_shows():
    return render_template("TestPage.html")


@app.route('/AdminViewAnimals')
def admin_view_animals():
    rows = Database.search_for_animals()
    # pass returned SQL query into HTML template
    return render_template("./AdminTemplates/addAnimal.html", rows=rows)

@app.route('/addAnimal')
def add_animal():
    animal = request.form['animalName']
    species = request.form['species']
    exhibit = request.form['exhibit']
    age = request.form['age']
    result = Database.add_animals(animal, species, exhibit, age)

    if isValidPassword(password):
        Database.showTables()
        result = Database.login(user, password)

        if result is not 0:
            # If user exists in database, find corresponding user type
            print("query returned valid username")
            session['email'] = user
            session['user_type'] = Database.get_userType(user)
            print("session user_type is: " + session['user_type'])
            return json.dumps({'status': 'OK', 'user': user, 'user_type': session['user_type']})
        else:
            print("User not found in resulted query")
            return json.dumps({'status': 'BAD', 'user': user, 'pass': 'error'})
    else:
        print("Error in login, invalid login data")
        return json.dumps({'status': 'BAD', 'user': user, 'pass': 'error'})

    rows = Database.search_for_animals()
    return render_template("./AdminTemplates/addAnimal.html", rows=rows)


@app.route('/addShow')
def add_show():
    return render_template("TestPage.html")


#
#
# # # # # # # # # # # # Pages Common to Visitor & Staff # # # # # # # # # # # #
#
#
# if needed, to be added later
#
#
# # # # # # # # # # # # Pages Common to Visitor & Admin # # # # # # # # # # # #
#
#
# if needed, to be added later
#
#
# # # # # # # # # # # # Pages Common to All # # # # # # # # # # # #
#
#


@app.route('/LogOut')
def Log_Out():
    print("User requests to Log Out, popping user's session variables")
    session.pop('email', None)
    session.pop('user_type', None)
    return render_template('Login.html')


#
#
# # # # # # # # # # # # Helper Functions # # # # # # # # # # # #
#
#


def isValidEmail(email):
    if len(email) > 6:
        if re.match("[^@]+@[^@]+\.[^@]+", email, re.IGNORECASE):
            print("valid Email, true returned")
            return True

    print("Invalid Email, false returned")
    return False


def isValidPassword(password):
    p_err = []
    if not (len(password) > 7):
        p_err.append(0)
    # if not (any(c.isdigit() for c in password)):
    # p_err.append(1)
    # if not (any(c.isupper() for c in password)):
    # p_err.append(2)

    if not p_err:
        print("valid password, true returned")
        return True
    else:
        print("Invalid password, false returned")
        return False


if __name__ == "__main__":
    app.run(debug=True)

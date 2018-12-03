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
    con = pymysql.connect(host=host, user=user, password=password, autocommit=False, db=db, charset=charSet,
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

    #
    # Extra data for testing- Visitor visits Exhibits - 2 visits to same exhibit should show a Count() of 2
    #
    add_exhibit_visit = """INSERT into ExhibitVisits values("xavier_swenson", "Pacific",Default);"""
    add_exhibit_visit_2 = """INSERT into ExhibitVisits values("xavier_swenson", "Pacific",Default);"""

    #
    # Extra data for testing- Visitor visits Show should show up in Show History
    #

    addShowVisit = """Insert into ShowVisits values ("Feed the Fish", "2018-10-08 12:00:00", "xavier_swenson");"""

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
        userType_query = "Select UserType FROM Users WHERE Users.Email = %s"
        cls.cur.execute(userType_query, email)
        result = cls.cur.fetchone()
        print("User type returned: " + str(result))
        return result['UserType']

    @classmethod
    def get_Username(cls, email):
        userType_query = "Select Username FROM Users WHERE Users.Email = %s"
        cls.cur.execute(userType_query, email)
        result = cls.cur.fetchone()
        print("Username returned: " + str(result))
        return result['Username']

    @classmethod
    def addto_StaffTable(cls, username):
        add_staff_query = "INSERT into Staff values (%s)"
        cls.cur.execute(add_staff_query, username)
        result = cls.cur.fetchone()
        print("Staff table added: " + str(result))

    @classmethod
    def addto_VisitorTable(cls, username):
        add_visitor_query = "INSERT into Visitor values (%s)"
        cls.cur.execute(add_visitor_query, username)
        result = cls.cur.fetchone()
        print("Visitor table added: " + str(result))

    @classmethod
    def register(cls, username, password, email, user_type):
        """
            Returns 0 if the SQL INSERT Operation fails, returns a non-zero value otherwise (INSERT successful)
        """
        print("register query provided parameters: " + username + ',' + password + "," + email + "," + user_type)

        register_query = "Insert into Users values (%s, %s, %s, %s)"
        try:
            result = cls.cur.execute(register_query, (username, password, email, user_type))

            print("Register Query returned: " + str(result))
            if result is not 0:
                return 1
            else:
                return 0

        except Exception as e:
            print("Exeception occured:{}".format(e))
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
    def exhibit_details_info(cls, exhibit_name):

        print("exhibit name for exhibit details: " + exhibit_name)

        exhibit_detail_query = (
            "SELECT Distinct e.ExhibitName, e.WaterFeature, e.Size, count(a.Exhibit = e.ExhibitName ) \n"
            "        as NumAnimals FROM Exhibits as e left join Animals as a on a.Exhibit = e.ExhibitName \n"
            "        where e.ExhibitName= %s   group by e.Size, e.ExhibitName, e.WaterFeature ")
        cls.cur.execute(exhibit_detail_query, exhibit_name)
        result = cls.cur.fetchone()
        print("Exhibit Detail info result: " + str(result))

        return result

    @classmethod
    def view_all_animals(cls):
        search_animals_query = (
            "SELECT DISTINCT a.AnimalName as Name, a.Species, a.Exhibit, a.Age, a.Type_of_Animal  \n"
            " as Type FROM Animals as a GROUP BY a.AnimalName, a.Species, a.Exhibit, a.Age, a.Type_of_Animal")
        cls.cur.execute(search_animals_query)
        result = cls.cur.fetchall()
        print("Search for animals result: " + str(result))

        return result

    @classmethod
    def view_exhibit_history(cls, username):
        exhibit_history_query = ("SELECT Distinct e.ExhibitName as Name, e.Date_Time as Time, count(*) over \n"
                                 "        ( partition by e.ExhibitName ) as \"Number of Visits\" from ExhibitVisits as e Where e.Visitor = %s""")
        cls.cur.execute(exhibit_history_query, username)
        result = cls.cur.fetchall()
        print("View Exhibit History result: " + str(result))

        return result

    @classmethod
    def search_shows(cls):
        get_shows_query = """SELECT s.ShowName as Name, s.LocatedAt as Exhibit, s.Date_Time as Date FROM Shows as s"""
        cls.cur.execute(get_shows_query)
        result = cls.cur.fetchall()
        print("search shows result: " + str(result))

        return result

    @classmethod
    def view_show_history(cls, username):
        show_history_query = """Select Distinct s.ShowName as Name, s.Date_Time as Time, shows.LocatedAt as Exhibit
                        From ShowVisits as s, Shows as shows where s.Visitor = %s and s.Date_Time = shows.Date_Time"""
        cls.cur.execute(show_history_query, username)
        result = cls.cur.fetchall()
        print("view show history result: " + str(result))

        return result

    @classmethod
    def log_show_visits(cls, show_name, date_time, username):

        print("log show visits variables: " + show_name + ", " + date_time + ", " + username)
        date_time_query_check = """SELECT * FROM ShowVisits  where %s <= NOW()"""
        log_show_query = "INSERT into ShowVisits values(%s, %s, %s) "

        try:
            date_check = cls.cur.execute(date_time_query_check, date_time)

            print("log show visits query returned: " + str(date_check))
            if date_check is not 0:
                result = cls.cur.execute(log_show_query, (str(show_name), str(date_time), str(username)))
                print("add log Show Visits returned: " + str(result))
                return 1
            else:
                return 0

        except Exception as e:

            print("Exeception occured:{}".format(e))
            return 0

    @classmethod
    def get_exhibit_animals(cls, exhibit_name):
        exhibit_animals_query = "SELECT AnimalName as Name, Species FROM Animals WHERE Exhibit= %s"
        cls.cur.execute(exhibit_animals_query, exhibit_name)
        result = cls.cur.fetchall()
        print("exhibit animals query: " + str(result))

        return result

    @classmethod
    def log_exhibit_visit(cls, username, exhibit_name):
        print("log exhibits vars provided: " + username + ", " + exhibit_name)
        try:
            log_exhibit_query = """INSERT into ExhibitVisits values(%s, %s ,Default)"""
            cls.cur.execute(log_exhibit_query, (username, exhibit_name))
            result = cls.cur.fetchone()
            print("log exhibit visit returned: " + str(result))
            if result is not 0:
                return 1
            else:
                return 0
        except Exception as e:
            print("Exception occurred:{}".format(e))
            return 0

    @classmethod
    def get_animal_details(cls, animal_name, animal_species):
        print("get animal details animal name provided: " + animal_name)
        animal_details_query = "Select * From Animals where AnimalName = %s and Species = %s"
        cls.cur.execute(animal_details_query, (animal_name, animal_species))
        result = cls.cur.fetchone()
        print("animal details returned: " + str(result))

        return result

    @classmethod
    def order_by_animals_attribute(cls, order_by_attr):
        print("order by animals attribute provided: " + order_by_attr)
        order_by_animal_query = """SELECT AnimalName as Name, Species FROM Animals WHERE Exhibit="Pacific" 
        order by %s"""

        cls.cur.execute(order_by_animal_query, order_by_attr)
        result = cls.cur.fetchall()
        print("order by animals column result: " + str(result))

        return result

    #
    #
    # # # # # # # # # # # # SQL Scripts for Staff # # # # # # # # # # # #
    #
    #

    @classmethod
    def get_animal_care_details(cls, animal_name, animal_species):
        print("get animal care details provided: " + animal_name + ", " + animal_species)
        animal_care_details_query = "Select * From Notes where AnimalName = %s and Species=%s"
        cls.cur.execute(animal_care_details_query, (animal_name, animal_species))

        result = cls.cur.fetchall()
        print("animal Care Details results set: " + str(result))
        return result

    @classmethod
    def add_animal_note(cls, username, staff_note, animal_name, animal_species, ):
        print("add animal note vars: " + username + ", " + animal_name + ", " + animal_species + ", " + staff_note)
        add_note_query = """Insert into Notes values(%s, default, %s, %s, %s)"""
        try:
            result = cls.cur.execute(add_note_query, (username, staff_note, animal_name, animal_species))
            print("log show visits query returned: " + str(result))
            if result is not 0:
                print("add log Show Visits returned: " + str(result))
                return 1
            else:
                return 0

        except Exception as e:

            print("Exeception occured:{}".format(e))
        return 0

    #
    #
    # # # # # # # # # # # # SQL Scripts for Admin # # # # # # # # # # # #
    #
    #

    @classmethod
    def add_animal(cls, animalname, species, exhibit, age, animaltype):
        """
        :rtype: returns an boolean of 1 if successful insertion of animal in the database, 0 otherwise
        """
        try:
            add_animal_query = """Insert into Animals values (%s, %s , %s, %s, %s)"""
            cls.cur.execute(add_animal_query, (animalname, species, exhibit, age, animaltype))
            result = cls.cur.fetchall()
            print("add animal result: " + str(result))

            return 1

        except Exception as e:
            print("Exception occurred:{}".format(e))
            return 0

    def delete_animal(cls, animalname, species):
        try:
            delete_animal_query = """DELETE FROM Animals WHERE (AnimalName = %s, Species = %s)"""
            cls.cur.execute(delete_animal_query, (animalname, species, exhibit, age, animaltype))
            result = cls.cur.fetchall()
            print("delete animal result: " + str(result))
            return 1
        except Exception as e:
            print("Exception occurred:{}".format(e))
            return 0

    @classmethod
    def add_shows(cls, show_name, date_time, located_at, hosted_by):
        try:
            add_show_query = """INSERT INTO SHOWS VALUES (%s, %s, %s, %s)"""
            cls.cur.execute(add_show_query, (show_name, date_time, located_at, hosted_by))
            result = cls.cur.fetchall()
            print("add show result: " + str(result))
            return 1

        except Exception as e:
            print("Exception occurred:{}".format(e))
            return 0

    @classmethod
    def search_visitors(cls):
        get_visitor_query = """SELECT s.Username as Username, s.Email as Email FROM Users as s 
          WHERE s.UserType='visitor'"""
        cls.cur.execute(get_visitor_query)
        result = cls.cur.fetchall()
        print("search staff result: " + str(result))
        return result

    @classmethod
    def search_staff(cls):
        get_staff_query = """SELECT s.Username as Username, s.Email as Email FROM Users as s WHERE s.UserType='staff'"""
        cls.cur.execute(get_staff_query)
        result = cls.cur.fetchall()
        print("search staff result: " + str(result))
        return result

    @classmethod
    def delete_user(cls, username):
        try:
            delete_user_query = """ DELETE FROM Users WHERE Username = %s """
            cls.cur.execute(delete_user_query, username)
            result = cls.cur.fetchall()
            print("delete user result: " + str(result))
            return 1

        except Exception as e:
            print("Exception occurred:{}".format(e))
            return 0

    @classmethod
    def delete_show(cls, show_name, date_time):
        print("Admin delete show provided vars: " + show_name + ", " + date_time)
        delete_show_q = """delete from Shows where Shows.ShowName=%s and Shows.Date_Time = %s"""

        try:
            cls.cur.execute(delete_show_q, (show_name, date_time))
            result = cls.cur.fetchone()
            print("delete show returned: " + str(result))
            return 1

        except Exception as e:
            print("Exception occurred:{}".format(e))
            return 0

    @classmethod
    def get_staff_list(cls):
        staff_list_query = "Select Username From Users where UserType=%s"
        user_type = "Staff"
        cls.cur.execute(staff_list_query, user_type)

        result = cls.cur.fetchall()
        print("staff List returned: " + str(result))
        return result


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
            session['username'] = Database.get_Username(user)
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

        print("result value of register is: " + str(result))
        if result is not 0:

            # Add user to respective staff or visitor table
            if visitor_userType == "staff":
                Database.addto_StaffTable(username)
            else:
                Database.addto_VisitorTable(username)

            print("returning valid json with status OK and setting current user session username and type")
            session['email'] = email
            session['user_type'] = Database.get_userType(email)
            session['username'] = username
            print("user type after registering is: " + str(session['user_type']))
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
    # Only for testing purposes- after testing completed, remove the if/else, session must contain a username
    if 'username' in session:
        rows = Database.view_exhibit_history(session['username'])
    else:
        rows = Database.view_exhibit_history("xavier_swenson")
    # pass returned SQL query into jinja HTML template
    return render_template("./VisitorTemplates/ExhibitHistory.html", rows=rows)


@app.route('/viewShows')
def view_shows():
    rows = Database.search_shows()
    return render_template('./VisitorTemplates/searchShows.html', rows=rows)


@app.route('/logShowVisit', methods=['POST'])
def log_show_visit():
    print("log show visit JSON request: " + str(request.json))

    # Only for testing purposes- after testing completed, remove the if/else, session must contain a username
    if 'username' in session:
        username = session['username']
    else:
        # Use default username of xavier_swenson
        username = "xavier_swenson"

    show_name = str(request.json['show_name'])
    exhibit = str(request.json['exhibit']).replace(" ", "").replace("\n", "")
    show_date = str(request.json['date_time'])

    print("log Show information before query: " + show_name + ", " + show_date + ", " + username)

    result = Database.log_show_visits(show_name, show_date, username)

    if result is not 0:
        return json.dumps({'status': 'OK'})
    else:
        return json.dumps({'status': 'BAD'})


@app.route('/viewShowHistory')
def view_show_history():
    # Only for testing purposes- after testing completed, remove the if/else, session must contain a username
    if 'username' in session:
        rows = Database.view_show_history(session['username'])
    else:
        rows = Database.view_show_history("xavier_swenson")
    # pass returned SQL query into jinja HTML template
    return render_template('./VisitorTemplates/ShowHistory.html', rows=rows)


@app.route('/SearchForAnimals')
def search_for_animals():
    rows = Database.view_all_animals()
    # pass returned SQL query into jinkja HTML template
    return render_template("./VisitorTemplates/searchAnimals.html", rows=rows)


@app.route('/ExhibitDetail', methods=['POST'])
def exhibit_detail():
    print("request from exhibit detail: " + str(request.json))
    exhibit_name = str(request.json['exhibit'])
    exhibit_name = exhibit_name.replace(" ", "").replace("\n", "")
    print("new exhibit name replaced: " + exhibit_name)

    exhibit_rows = Database.exhibit_details_info(exhibit_name)
    exhibit_animals_row = Database.get_exhibit_animals(exhibit_name)
    return render_template("./VisitorTemplates/ExhibitDetail.html", exhibit=exhibit_rows,
                           animals_row=exhibit_animals_row)


@app.route('/LogExhibitVisit', methods=['POST'])
def log_exhibit_visit():
    print("request json for log exhibit visit: " + str(request.json))

    if 'username' in session:
        username = session['username']
    else:
        # Use default username of xavier_swenson
        username = "xavier_swenson"

    exhibit_name = str(request.json['exhibit'])
    exhibit_name = exhibit_name.replace("Name: ", "").replace(" ", "")
    result = Database.log_exhibit_visit(username, exhibit_name)

    print("result returned back for Log Exhibit Visits: " + str(result))
    if result is not 0:
        return json.dumps({'status': 'OK'})
    else:
        return json.dumps({'status': 'BAD'})


@app.route('/AnimalDetails', methods=['POST'])
def animal_details():
    print("request json for Animal Details: " + str(request.json))
    animal_name = str(request.json['animal'])
    animal_name = animal_name.strip().replace("\n", "")
    animal_species = str(request.json['species'])
    print("animal_name for animal Details: " + animal_name + ", species: " + animal_species)
    animal_row = Database.get_animal_details(animal_name, animal_species)
    return render_template('./VisitorTemplates/AnimalDetail.html', animal=animal_row)


#
#
# # # # # # Staff Pages (excluding /LogOut) # # # # # #
#
#

@app.route('/StaffSearchAnimals')
def search_animals():
    rows = Database.view_all_animals()
    return render_template("./StaffTemplates/StaffSearchAnimals.html", rows=rows)


@app.route('/StaffViewShows')
def staff_view_shows():
    rows = Database.search_shows()
    return render_template("./StaffTemplates/StaffViewShows.html", rows=rows)


@app.route('/AnimalCare', methods=['POST'])
def render_animal_care():
    print("request json for Animal Care: " + str(request.json))
    animal_name = str(request.json['animal'])
    animal_name = animal_name.strip().replace("\n", "")
    animal_species = str(request.json['species'])

    animal_data = Database.get_animal_details(animal_name, animal_species)
    notes_data = Database.get_animal_care_details(animal_name, animal_species)

    return render_template("./StaffTemplates/AnimalDetail.html", animal_data=animal_data, notes_data=notes_data)


@app.route('/LogStaffNote', methods=['POST'])
def log_staff_note():
    print("request json for log staff note: " + str(request.json))

    # for testing purposes only
    if 'username' in session:
        username = session['username']
    else:
        # Use default username of xavier_swenson
        username = "staff"

    animal_name = str(request.json['animal'])
    animal_name = animal_name.replace("Name: ", "")
    animal_species = str(request.json['species'])
    animal_species = animal_species.replace("Species: ", "")
    staff_note = str(request.json['staff_note'])
    print("final log staff note query vars: " + username + ", " + animal_name + ", " + animal_species + ", "
          + staff_note)
    result = Database.add_animal_note(username, staff_note, animal_name, animal_species)

    if result is not 0:
        return json.dumps({'status': 'OK', 'animal_name': animal_name, 'animal_species': animal_species})
    else:
        return json.dumps({'status': 'BAD'})


#
#
# # # # # # # # Admin Pages Below (excluding /LogOut) # # # # # # # #
#
#

@app.route('/viewVisitors')
def view_visitors():
    rows = Database.search_visitors()
    return render_template('./AdminTemplates/viewVisitors.html', rows=rows)


@app.route('/viewStaff')
def view_staff():
    rows = Database.search_staff()
    return render_template('./AdminTemplates/viewStaff.html', rows=rows)


@app.route('/AdminViewShows')
def admin_view_shows():
    rows = Database.search_shows()
    # inject SQL data into jinja html template
    return render_template('./AdminTemplates/viewShows.html', rows=rows)


@app.route('/addShow')
def add_show():
    rows = Database.get_staff_list()
    return render_template("./AdminTemplates/addShow.html", rows=rows)


@app.route('/addShowValidation', methods=['POST'])
def add_show_query():
    print("add_show Request Received from Admin")
    show_name = request.form['showName']
    date = request.form['date']
    time = request.form['time']
    hosted_by = request.form['staff_name']
    exhibit_name = request.form['exhibit_name']

    time = str(time)
    date = str(date)

    # concatenate the date and time to produce a searchable SQL query, for example:
    # 2017-01-01, 01:01 -> "2017-01-01 01%", which means if this host (staff) has another date with
    # a matching minute, that means they can't add a show at that minute, they should schedule a show later
    date_time = date + " " + time[:2] + "%"
    result = Database.add_shows(show_name, date_time, exhibit_name, hosted_by)

    print("add_show date_time final: " + str(result))
    if result is not 0:
        print("returning json with status OK")
        return json.dumps({'status': 'OK'})
    else:
        print("returning json with status BAD")
        return json.dumps({'status': 'BAD'})


@app.route('/AdminViewAnimals')
def admin_view_animals():
    rows = Database.view_all_animals()
    # inject SQL data into jinja html template
    return render_template("./AdminTemplates/viewAnimals.html", rows=rows)


@app.route('/AddAnimalsPage')
def admin_add_animals():
    rows = Database.view_all_animals()
    # inject SQL data into jinja html template
    return render_template("./AdminTemplates/addAnimal.html", rows=rows)


@app.route('/addAnimal', methods=['POST'])
def add_animal_query():
    print("add_animal Request Received from Admin")
    animal_name = request.form['animalName']
    species = request.form['species']
    exhibit = request.form['exhibit_name']
    age = request.form['age']
    animal_type = request.form['animal_type']

    result = Database.add_animal(animal_name, species, exhibit, age, animal_type)

    if result is not 0:
        print("returning json with status OK")
        return json.dumps({'status': 'OK'})
    else:
        print("returning json with status BAD")
        return json.dumps({'status': 'BAD'})

@app.route('/deleteAnimal', methods=['POST'])
def delete_animal_query():
    print("Delete Animal request received from Admin")
    show_info = request.form['show']
    s = show_info.strip().split(",")
    animalname = s[0].replace("[", "")
    species = s[1].replace("]", "")
    print("delete show show_name: " + show_name)
    result = Database.delete_animal(animalname, species)

    if result is not 0:
        print("user deleted successfully, returning json with status OK")
        return json.dumps({'status': 'OK'})
    else:
        print("user not deleted, error: returning json with status BAD")
        return json.dumps({'status': 'BAD'})

@app.route('/deleteVisitor', methods=['POST'])
def delete_visitor_query():
    print("Delete Visitor User request received from Admin")
    username = request.form['user']
    print("Username to be deleted: " + username)

    result = Database.delete_user(username)

    if result is not 0:
        print("user deleted successfully, returning json with status OK")
        return json.dumps({'status': 'OK'})
    else:
        print("user not deleted, error: returning json with status BAD")
        return json.dumps({'status': 'BAD'})


@app.route('/deleteStaff', methods=['POST'])
def delete_staff_query():
    print("Delete Staff User request received from Admin")
    username = request.form['user']
    print("Username to be deleted: " + username)

    result = Database.delete_user(username)

    if result is not 0:
        print("returning json with status OK")
        return json.dumps({'status': 'OK'})
    else:
        print("returning json with status BAD")
        return json.dumps({'status': 'BAD'})


@app.route('/deleteShow', methods=['POST'])
def delete_show_query():
    print("delete show user request recieved from Admin")
    show_info = request.form['show']
    s = show_info.strip().split(",")
    show_name = s[0].replace("[","")
    show_time = s[1].replace("]", "")
    print("delete show show_name: " + show_name)
    result = Database.delete_show(show_name,show_time)
    if result is not 0:
        print("returning json with status OK")
        return json.dumps({'status': 'OK'})
    else:
        print("returning json with status BAD")
        return json.dumps({'status': 'BAD'})


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

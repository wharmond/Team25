from flask import Flask, render_template, request, json
import pymysql, re
import hashlib

app = Flask(__name__)


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

    @classmethod
    def list_employees(self):
        self.cur.execute("SELECT first_name, last_name, gender FROM employees LIMIT 50")
        result = self.cur.fetchall()
        return result

    @classmethod
    def login(cls, email, user_pass):
        print("login: email: " + email + ", pass: " + user_pass)

        # Query matches email field and password to Users table in database, returns boolean 0 if not found, 1 otherwise
        login_query = "SELECT * FROM Users WHERE Users.Email = %s AND Users.Password = %s"
        result = cls.cur.execute(login_query, (email, user_pass))
        print("Query returned: " + str(result))

        return result

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
        result = cls.cur.execute(Register_query, (username, password, email, user_type))
        print("Register Query returned: " + str(result))

        return result

    @classmethod
    def showTables(cls):
        cls.cur.execute("show tables")
        rows = cls.cur.fetchall()
        for row in rows:
            print(row)


@app.route("/")
def hello():
    return render_template('Login.html')


@app.route("/signIn", methods=['POST'])
def signIn():
    user = request.form['username']
    # session['username'] = user
    password = request.form['password']

    if isValidPassword(password):
        Database.showTables()
        result = Database.login(user, password)

        if result is not None:
            print("query returned valid username")
            return json.dumps({'status': 'OK', 'user': user, 'pass': password})
        else:
            print("User not found in resulted query")
            return json.dumps({'status': 'BAD', 'user': user, 'pass': 'error'})
    else:
        print("Error in inputs")
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
            visitor_userType = "Staff"
        else:
            print("Staff checkbox in Registration page NOT checked")
            visitor_userType = "Visitor"

        result = Database.register(username, password, email, visitor_userType)
        print("result value: " + str(result))

        if result is not None:
            print("returning valid json with status OK")
            return json.dumps({'status': 'OK', 'email': email, 'pass': password})
        else:
            print("returning json with status BAD")
            return json.dumps({'status': 'BAD', 'email': email, 'pass': 'error'})

    else:
        print("Invalid email or password input provided or User Exists in database: " + email + ", pass: " + password)
        return json.dumps({'status': 'BAD', 'email': email, 'pass': 'error', 'error': 'User_Exists'})


@app.route("/addNote")
def addNote():
    return (json.dumps({'status': 'OK', 'note': note}))


@app.route("/signUp")
def signUp():
    return render_template('signUp.html')


@app.route('/visitorHomePage')
def visitor_homepage():
    return render_template("Visitor_Homepage.html")


@app.route('/searchExhibits')
def search_exhibits():
    return render_template("TestPage.html")


@app.route('/viewExhibitHistory')
def view_exhibit_history():
    return render_template("TestPage.html")


@app.route('/viewShows')
def view_shows():
    return render_template("TestPage.html")


@app.route('/viewShowHistory')
def view_show_history():
    return render_template("TestPage.html")


@app.route('/SearchAnimals')
def search_for_animals():
    return render_template("TestPage.html")


@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user = request.form['username'];
    # session['username'] = user
    password = request.form['password'];
    p_err = []
    if not (len(password) > 6):
        p_err.append(0)
    if not (any(c.isdigit() for c in password)):
        p_err.append(1)
    if not (any(c.isupper() for c in password)):
        p_err.append(2)
    if not p_err:
        return (json.dumps({'status': 'OK', 'user': user, 'pass': password}))
    else:
        return (json.dumps({'status': 'BAD', 'user': user, 'pass': p_err}))


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
    if not (any(c.isdigit() for c in password)):
        p_err.append(1)
    if not (any(c.isupper() for c in password)):
        p_err.append(2)

    if not p_err:
        print("valid password, true returned")
        return True
    else:
        print("Invalid password, false returned")
        return False


if __name__ == "__main__":
    app.run(debug=True)

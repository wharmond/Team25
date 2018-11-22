from flask import Flask, render_template, request, json
import pymysql
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

    # Create the connection with configured parameters
    con = pymysql.connect(host=host, user=user, password=password, db=db, charset=charSet,
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
    def login(cls, user, user_pass):
        print("login: user: " + user + ", pass: " + user_pass)

        # Query matches email field and password to Users table in database, returns boolean 0 if not found, 1 otherwise
        login_query = "SELECT * FROM Users WHERE exists (SELECT * FROM Users WHERE Users.Email = %s AND Users.Password = %s )"
        print("Query returned: " + str(cls.cur.execute(login_query, (user, user_pass))))
        result = cls.cur.fetchone()

        return result

    # TODO
    @classmethod
    def register(cls, name):
        return ''

    @classmethod
    def showTables(cls):
        cls.cur.execute("show tables")
        rows = cls.cur.fetchall()
        for row in rows:
            print(row)


@app.route("/")
def hello():
    return (render_template('Login.html'))


@app.route("/signIn", methods=['POST'])
def signIn():
    user = request.form['username']
    # session['username'] = user
    password = request.form['password']

    p_err = []
    if not (len(password) > 7):
        p_err.append(0)
    if not (any(c.isdigit() for c in password)):
        p_err.append(1)
    if not (any(c.isupper() for c in password)):
        p_err.append(2)

    # Implement SQL queries here for signing in #

    if p_err == []:
        Database.showTables()
        result = Database.login(user, password)

        if result:
            print("query returned valid username")
            return (json.dumps({'status': 'OK', 'user': user, 'pass': password}))
        else:
            print("User not found in resulted query")
            return (json.dumps({'status': 'BAD', 'user': user, 'pass': p_err}))
    else:
        print("Error in inputs")
        return (json.dumps({'status': 'BAD', 'user': user, 'pass': p_err}))


@app.route('/Register')
def Register():
    return render_template("TestPage.html")


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
    if not (len(password) > 7):
        p_err.append(0)
    if not (any(c.isdigit() for c in password)):
        p_err.append(1)
    if not (any(c.isupper() for c in password)):
        p_err.append(2)
    if p_err == []:
        return (json.dumps({'status': 'OK', 'user': user, 'pass': password}))
    else:
        return (json.dumps({'status': 'BAD', 'user': user, 'pass': p_err}))


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, json
import pymysql
import hashlib

## from flask.ext.mysql import MySQL

app = Flask(__name__)

class Database:
    def __init__(self):
        host = "..."
        user = "..."
        password = "..."
        db = "..."
        
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
        
        def list_employees(self):
            self.cur.execute("SELECT first_name, last_name, gender FROM employees LIMIT 50")
            result = self.cur.fetchall()
            return result

@app.route("/")
def hello():
    return(render_template('hello.html'))

@app.route("/addNote")
def addNote():
    return(json.dumps({'status':'OK','note':note}))

@app.route("/registration")
def register():
    return(render_template('Registration.html'))

@app.route('/registerUser', methods=['POST'])
def registerUser():
    user =  request.form['username'];
    password = request.form['password'];
    p_err = []
    if not (len(password)>7):
        p_err.append(0)
    if not (any(c.isdigit() for c in password)):
        p_err.append(1)
    if not (any(c.isupper() for c in password)):
        p_err.append(2)
    if p_err == []:
        return(json.dumps({'status':'OK','user':user,'pass':password}))
    else:
        return(json.dumps({'status':'BAD','user':user,'pass':p_err}))

if __name__ == "__main__":
    app.run(debug= True)

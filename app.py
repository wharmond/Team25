from flask import Flask, render_template, request, json, session

##from flask.ext.mysql import MySQL

app = Flask(__name__)


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
        return (json.dumps({'status': 'OK', 'user': user, 'pass': password}))
    else:
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

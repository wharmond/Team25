from flask import Flask,render_template, request,json
app = Flask(__name__)

@app.route("/")
def hello():
    return(render_template('hello.html'))

@app.route("/signUp")
def signUp():
    return(render_template('signUp.html'))

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
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
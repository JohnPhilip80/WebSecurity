from flask import Flask, render_template,redirect,url_for,request,make_response

import dbService
from dbService import *
import uuid

app = Flask(__name__)

@app.route("/")
@app.route("/Home")
def Home():
    return render_template("home.html")

@app.route("/Aboutus")
def Aboutus():
    return render_template("aboutus.html")

@app.route("/Contactus")
def Contactus():
    return render_template("contactus.html")

@app.route("/Accounts")
def Accounts():
    return render_template("accounts.html")




@app.route("/Dashboard")
def Dashboard():
    sessionId = request.cookies.get('SESSION_ID')
    if not sessionId:
        return redirect('/')
    user = dbService.getUserBySessionId(sessionId)
    if not user:
        return redirect('/')
    return render_template("dashboard.html",user = user)

"""
@app.route("/Dashboard/<userName>")
def Dashboard(userName):
    return render_template("dashboard.html",userName=userName)
"""

@app.route("/Login",methods=["GET","POST"])
def Login():
    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        user = dbService.getUserByCredentials(userName,password)
        if user:
            sessionId = str(uuid.uuid4())
            dbService.createSessionForUser(user["user_id"],sessionId)
            response = make_response(redirect('/Dashboard'))
            response.set_cookie("SESSION_ID", sessionId)  # manual cookie
            return response
        return "Invalid Credentials"
    else:
        return render_template("login.html")

@app.route("/Logout")
def Logout():
    sessionId = request.cookies.get("SESSION_ID")
    if sessionId:
        dbService.deleteSession(sessionId)
    response = make_response(redirect('/Home'))
    response.delete_cookie("SESSION_ID")
    return response

@app.route("/Register")
def Register():
    return render_template("register.html")

@app.route("/Transaction",methods=["GET","POST"])
def Transaction():
    sessionId = request.cookies.get('SESSION_ID')
    if not sessionId:
        return redirect('/')
    if request.method == 'POST':
        toUser = request.form['toUser']
        transferAmount = request.form['transferAmount']
        dbService.transferMoney(sessionId,toUser,transferAmount)
        return redirect('/Dashboard')
    return render_template("transaction.html")

@app.route("/Chat",methods=["GET","POST"])
def Chat():
    sessionId = request.cookies.get('SESSION_ID')
    if not sessionId:
        return redirect('/')
    if request.method == 'POST':
        userComment = request.form['userComment']
        dbService.sendUserComment(sessionId,userComment)
        return None
    else:
        userComments = dbService.getAllComments()
        return render_template("chat.html",userComments = userComments)

if __name__ == '__main__':
    app.run(debug=True)
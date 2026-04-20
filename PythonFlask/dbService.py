import mysql.connector
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="db_bank",
    )
def getUserByCredentials(username, password):
    con=get_connection()
    cur=con.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE login_name = %s and login_password = %s",(username,password))
    user = cur.fetchone()
    con.close()
    return user

def createSessionForUser(userId, sessionId):
    con=get_connection()
    cur=con.cursor(dictionary=True)
    cur.execute("INSERT INTO sessions (session_id, user_id) VALUES (%s, %s)",(sessionId,userId))
    con.commit()
    con.close()

def getUserBySessionId(sessionId):
    con=get_connection()
    cur=con.cursor(dictionary=True)
    cur.execute("SELECT a.login_name, b.balance_amount FROM sessions c INNER JOIN users a ON c.user_id = a.user_id INNER JOIN accounts b ON c.user_id = b.user_id WHERE c.session_id= %s", (sessionId,))
    user = cur.fetchone()
    con.close()
    return user

def deleteSession(sessionId):
    con=get_connection()
    cur=con.cursor(dictionary=True)
    cur.execute("DELETE FROM sessions WHERE session_id = %s", (sessionId,))
    con.commit()
    con.close()

def transferMoney(sessionId, toUser, transferAmount):
    fromUser = getUserBySessionId(sessionId)["login_name"]
    con=get_connection()
    cur=con.cursor(dictionary=True)
    cur.execute("update db_bank.accounts set balance_amount = balance_amount - %s where user_id = (select user_id from db_bank.users where login_name= %s );",(transferAmount,fromUser))
    con.commit()
    con.close()
    con = get_connection()
    cur = con.cursor(dictionary=True)
    cur.execute("update db_bank.accounts set balance_amount = balance_amount + %s where user_id = (select user_id from db_bank.users where login_name= %s );",(transferAmount, toUser))
    con.commit()
    con.close()

def sendUserComment(sessionId, comment):
    fromUser = getUserBySessionId(sessionId)["login_name"]
    con=get_connection()
    cur=con.cursor(dictionary=True)
    cur.execute("INSERT INTO user_comments(username, comment) VALUES (%s, %s), ?)",(fromUser,comment))
    con.commit()
    con.close()

def getAllComments():
    con=get_connection()
    cur=con.cursor(dictionary=True)
    cur.execute("SELECT * FROM user_comments")
    comments = cur.fetchall()
    con.close()
    userComments = ""
    for comment in comments:
        userComments = userComments + "<p><b>" + comment["username"] + ":</b> " + comment["comment"] + "</p>"
    return userComments

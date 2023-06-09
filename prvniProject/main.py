import mysql.connector
from flask import Flask, render_template
from flask import send_from_directory
from flask import request
from flask import jsonify
from flask import flash, redirect, url_for
import hashlib, uuid
import logging
import os 

logging.basicConfig(level=logging.DEBUG)

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    database="test"
)

mycursor = mydb.cursor(buffered=True)

mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)


print(mycursor.rowcount, "record inserted.")

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

salt = "uuid.uuid4().hex"

def GetHashedPass(password):
    hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode("utf-8")).hexdigest()
    return hashed_password

print(GetHashedPass("nwm"))
print(GetHashedPass("nwm"))

def get_my_ip(jmZakaznik):
    ip = request.remote_addr
    print(ip)
    sql = "INSERT INTO counter (IPv4, jmZakaznik) VALUES (%s,%s)"
    val = (ip, jmZakaznik)
    mycursor.execute(sql, val)
    mydb.commit()
    return jsonify({'ip': request.remote_addr}), 200


@app.route('/', methods=["GET", "POST"])
def home():
    jmZakaz = ""
    password = ""
    if request.method == "POST":
        jmZakaz = request.form["jmZakaznik"]
        password = request.form["password"]
        print(jmZakaz)
        print(password)
    password = GetHashedPass(password)
    sql = "SELECT *FROM users WHERE username ='%s' AND password ='%s'" % (jmZakaz, password)
    logging.debug("login sql: %s", sql)
    loginCursor = mydb.cursor(buffered=True)
    
    try:
        loginCursor.execute(sql)
        loginResults = loginCursor.fetchone()
        logging.debug("loginResults: %s", loginResults)
        if loginResults == None:
            flash("not such user")
        else:
            flash("logged in")

    except mysql.connector.Error as err:
        flash("Something went wrong: {}".format(err))


    get_my_ip(jmZakaz)
    mycursor.execute("SELECT count(IPv4) FROM counter")
    counter = mycursor.fetchone()
    print(counter)
    
    return render_template('index.html', counter=counter, zakaznik = jmZakaz)


@app.route("/templates/<path:path>")
def script(path):
    response = send_from_directory('templates', path)
    response.direct_passthrough = False
    print(response.get_data())
    return response


for x in mycursor:
    print(x)

def main():
    app.run(host="127.0.0.1", debug=True)

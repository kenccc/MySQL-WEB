import mysql.connector
from flask import Flask, render_template
from flask import send_from_directory
from flask import request
from flask import jsonify

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
    if request.method == "POST":
        jmZakaz = request.form["jmZakaznik"]
        print(jmZakaz)

    get_my_ip(jmZakaz)
    mycursor.execute("SELECT count(IPv4) FROM counter")
    counter = mycursor.fetchone()
    print(counter)

    return render_template('index.html', counter=counter, jmZakaz=jmZakaz)


@app.route("/templates/<path:path>")
def script(path):
    response = send_from_directory('templates', path)
    response.direct_passthrough = False
    print(response.get_data())
    return response


for x in mycursor:
    print(x)

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)

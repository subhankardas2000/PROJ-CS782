from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite database configuration
DATABASE = "database.db"

def create_table():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user_query (id INTEGER PRIMARY KEY, name TEXT, email TEXT, message TEXT)")

create_table()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('abouttab.html')

@app.route('/contact')
def contact():
    return render_template('contacttab.html')

@app.route('/conme', methods=['POST', 'GET'])
def conme():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']

            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user_query (name, email, message) VALUES (?, ?, ?)", (name, email, message))
                con.commit()
                msg = "Message Send Successfully!!"

        except Exception as e:
            print(e)
            con.rollback()
            msg = "Error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
    
    return render_template("contacttab.html")

@app.route('/coninfo')
def coninfo():
    with sqlite3.connect(DATABASE) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM user_query")
        rows = cur.fetchall()

    return render_template("coninfo.html", rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
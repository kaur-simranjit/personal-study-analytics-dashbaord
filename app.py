from flask import Flask
import sqlite3

# create flask app
app = Flask(__name__)

# database file name
db_name = "dashboard.db"

# connect to database
def connect_db():
    con_db = sqlite3.connect(db_name)
    con_db.row_factory = sqlite3.Row
    return con_db

# create database table
def init_db():
    con_db = connect_db()
    con_db.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   date TEXT NOT NULL,
                   course_studied TEXT NOT NULL,
                   study_method TEXT NOT NULL,
                   study_hours REAL NOT NULL,
                   break_time INTEGER NOT NULL,
                   productivity_rating INTEGER NOT NULL
        )
    """)
    con_db.commit()
    con_db.close()

@app.route("/")
def home():
    return "Working!"

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
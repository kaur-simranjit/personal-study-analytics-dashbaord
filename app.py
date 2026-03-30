from flask import Flask, redirect, render_template, request, url_for
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

# add a study session
@app.route("/add", methods=["GET", "POST"])
def add_study_session():
    if request.method == "POST":
        date = request.form["date"]
        course_studied = request.form["course_studied"]
        study_method = request.form["study_method"]
        study_hours = request.form["study_hours"]
        break_time = request.form["break_time"]
        productivity_rating = request.form["productivity_rating"]

        con_db = connect_db()
        con_db.execute("""
            INSERT INTO study_sessions(date, course_studied, study_method, 
                       study_hours, break_time, productivity_rating)
                       VALUES (?, ?, ?, ?, ?, ?) """,
                       (date, course_studied, study_method, study_hours, break_time, 
                        productivity_rating))
        con_db.commit()
        con_db.close()

        return redirect(url_for("home"))
    return render_template("add_study_session.html")

# view all saved study sessions
@app.route("/view")
def view_sessions():
    con_db = connect_db()
    sessions = con_db.execute("""
        SELECT * FROM study_sessions ORDER BY date DESC, id DESC
    """).fetchall()
    con_db.close()

    return render_template("view.html", sessions=sessions)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
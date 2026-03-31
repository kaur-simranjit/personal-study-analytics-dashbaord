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


# create a dashboard
@app.route("/")
def dashboard():
    con_db = connect_db()

    # total study sessions
    entries = con_db.execute("SELECT COUNT(*) AS total_entries FROM study_sessions"
                             ).fetchone() ["total_entries"]
    
    # total study hours
    total_study_hours = con_db.execute("""SELECT COALESCE(SUM(study_hours), 0) AS total_study_hours 
                                       FROM study_sessions""").fetchone() ["total_study_hours"]
    
    # avgerage productivity rating
    avg_productivity = con_db.execute("""SELECT COALESCE(AVG(productivity_rating), 0) AS avg_productivity
                                       FROM study_sessions""").fetchone() ["avg_productivity"]
    
    # average break time
    avg_break_time = con_db.execute("""SELECT COALESCE(AVG(break_time), 0) AS avg_break_time
                                       FROM study_sessions""").fetchone() ["avg_break_time"]
    
    # study hours over time
    time_and_hours = con_db.execute("""SELECT date, SUM(study_hours) AS total_hours FROM study_sessions 
                                    GROUP BY date ORDER BY date""").fetchall()
    
    dates = [row["date"] for row in time_and_hours]
    hours = [row["total_hours"] for row in time_and_hours]

    con_db.close()

    return render_template("dashboard.html", entries = entries, total_study_hours=round(total_study_hours, 2), 
                           avg_productivity=round(avg_productivity, 2), avg_break_time=round(avg_break_time, 2),
                           dates=dates, hours=hours)

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

        return redirect(url_for("dashboard"))
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
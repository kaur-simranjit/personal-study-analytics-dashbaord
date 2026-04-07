import os
from flask import Flask, redirect, render_template, request, url_for
import sqlite3
from datetime import datetime, timedelta

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
                   productivity_rating INTEGER NOT NULL)""")
    con_db.commit()
    con_db.close()

# create a dashboard
@app.route("/")
def dashboard():
    con_db = connect_db()

    # filter by time range
    filters = request.args.get("filter", "all")
    latest_row_date = con_db.execute("""SELECT MAX(date) AS latest_date
                                      FROM study_sessions""").fetchone()
    latest_date = latest_row_date["latest_date"]
    where_clause = ""
    params = []

    if latest_date:
        reference_date = datetime.strptime(latest_date, "%Y-%m-%d")
        
        if filters == "7": 
            start_date = (reference_date - timedelta(days=6)).strftime("%Y-%m-%d")
            where_clause = "WHERE date BETWEEN ? AND ?"
            params = [start_date, latest_date]
        
        elif filters == "30":
            start_date = (reference_date - timedelta(days=29)).strftime("%Y-%m-%d")
            where_clause = "WHERE date BETWEEN ? AND ?"
            params = [start_date, latest_date]

    # total study sessions
    entries = con_db.execute(f"""SELECT COUNT(*) AS total_entries 
                             FROM study_sessions 
                             {where_clause}""", params).fetchone() ["total_entries"]
    
    # total study hours
    total_study_hours = con_db.execute(f"""SELECT COALESCE(SUM(study_hours), 0) AS total_study_hours 
                                       FROM study_sessions 
                                       {where_clause}""", params).fetchone() ["total_study_hours"]
    
    # avgerage productivity rating
    avg_productivity = con_db.execute(f"""SELECT COALESCE(AVG(productivity_rating), 0) AS avg_productivity
                                      FROM study_sessions 
                                      {where_clause}""", params).fetchone() ["avg_productivity"]
    
    # average break time
    avg_break_time = con_db.execute(f"""SELECT COALESCE(AVG(break_time), 0) AS avg_break_time
                                    FROM study_sessions 
                                    {where_clause}""", params).fetchone() ["avg_break_time"]
    
    # study hours over time
    time_and_hours = con_db.execute(f"""SELECT date, SUM(study_hours) AS total_hours 
                                    FROM study_sessions 
                                    {where_clause} 
                                    GROUP BY date 
                                    ORDER BY date""", params).fetchall()
    
    study_label = [
        datetime.strptime(row["date"], "%Y-%m-%d").strftime("%b %-d")
        for row in time_and_hours
    ]
    study_value = [row["total_hours"] for row in time_and_hours]

    # productivity over time
    productivity_over_time = con_db.execute(f"""SELECT date, AVG(productivity_rating) AS avg_productivity_rating
                                            FROM study_sessions 
                                            {where_clause} 
                                            GROUP BY date 
                                            ORDER BY date""", params).fetchall()
    
    productivity_label = [
        datetime.strptime(row["date"], "%Y-%m-%d").strftime("%b %-d") 
        for row in productivity_over_time]
    productivity_value = [row["avg_productivity_rating"] for row in productivity_over_time]

    # time spent per course
    time_on_course = con_db.execute(f"""SELECT course_studied, SUM(study_hours) AS total_course_hours 
                                    FROM study_sessions 
                                    {where_clause} 
                                    GROUP BY course_studied 
                                    ORDER BY total_course_hours DESC""", params).fetchall()
    
    course_label = [row["course_studied"] for row in time_on_course]
    course_value = [row["total_course_hours"] for row in time_on_course]

    # average productivity by study method
    productivity_by_method = con_db.execute(f"""SELECT study_method, AVG(productivity_rating) AS productivity 
                                            FROM study_sessions 
                                            {where_clause} 
                                            GROUP BY study_method""", params).fetchall()
    
    method_label = [row["study_method"] for row in productivity_by_method]
    method_value = [row["productivity"] for row in productivity_by_method]

    con_db.close()

    return render_template("dashboard.html", entries = entries, total_study_hours=round(total_study_hours, 2), 
                           avg_productivity=round(avg_productivity, 2), avg_break_time=round(avg_break_time, 2),
                           study_label=study_label, study_value=study_value, productivity_label=productivity_label, 
                           productivity_value=productivity_value,course_label=course_label, course_value=course_value,
                           method_label=method_label, method_value=method_value, filters=filters)

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
        con_db.execute("""INSERT INTO study_sessions
                       (date, course_studied, study_method, study_hours, break_time, productivity_rating)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                       (date, course_studied, study_method, study_hours, break_time, productivity_rating))
        con_db.commit()
        con_db.close()

        return redirect(url_for("dashboard"))
    return render_template("add_study_session.html")

# view all saved study sessions
@app.route("/view")
def view_sessions():
    con_db = connect_db()
    sessions = con_db.execute("""SELECT * FROM study_sessions 
                              ORDER BY date DESC, id DESC""").fetchall()
    con_db.close()

    return render_template("view.html", sessions=sessions)

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
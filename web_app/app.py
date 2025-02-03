# ./web_app/app.py
from scripts.build_calendar import CalendarBuild
from scripts.build_todo import TodoBuild
from flask import Flask, render_template, url_for, redirect, session, request
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/home', methods=['GET'])
def home():
    current_time = datetime.now()
    if 'month' not in session or 'year' not in session:
        session['month'] = current_time.month
        session['year'] = current_time.year

    if 'month_display' not in session:
        session['month-display'] = True

    month = session['month']
    year = session['year']

    current_day = current_time.day
    current_month = current_time.month
    current_year = current_time.year

    calendar = CalendarBuild(month, year)
    month_name = calendar.get_month_name()
    month_layout = calendar.get_layout_month()
    year_layout = calendar.get_layout_year()
    num_of_weeks = len(month_layout[0])

    todo_list = TodoBuild.todo_list

    return render_template(
        'index.html',
        month_name = month_name,
        month_num = month,
        year = year,
        current_day = current_day,
        current_month = current_month,
        current_year = current_year,
        month_layout=month_layout,
        num_of_weeks=num_of_weeks,
        year_layout=year_layout,
        todo_list=todo_list
    )

@app.route('/prev_month', methods=['POST'])
def prev():
    month = session['month']
    year = session['year']

    if session['month_display']:
        month -= 1
        if month < 1:
            month = 12
            year -= 1
    else:
        year -= 1

    session['month'] = month
    session['year'] = year

    return redirect(url_for('home'))

@app.route('/next_month', methods=['POST'])
def next():
    month = session['month']
    year = session['year']

    if session['month_display']:
        month += 1
        if month > 12:
            month = 1
            year += 1
    else:
        year += 1

    session['month'] = month
    session['year'] = year

    return redirect(url_for('home'))

@app.route('/year_display', methods=['POST'])
def year_display():
    session['month_display'] = False
    return redirect(url_for('home'))

@app.route('/month_display', methods=['POST'])
def month_display():
    session['month_display'] = True
    return redirect(url_for('home'))

@app.route('/new_task', methods=['POST'])
def new_task():
    task = request.form.get('task', '')
    TodoBuild(task)
    return redirect(url_for('home'))

@app.route('/delete_task', methods=['POST'])
def delete_task():
    task = request.form.get('task', '')
    TodoBuild.delete_task(task)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=8000, debug=True)
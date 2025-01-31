# ./web_app/app.py
from scripts.build_calendar import CalendarBuild
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/home')
def home():
    calendar = CalendarBuild(1, 2025)

    month_layout = calendar.get_layout()
    num_of_weeks = len(month_layout[0])
    month_name = calendar.get_month_name()

    return render_template(
        'index.html',
        month_layout=month_layout,
        num_of_weeks=num_of_weeks,
        month_name = month_name
    )

if __name__ == '__main__':
    app.run(port=8000, debug=True)
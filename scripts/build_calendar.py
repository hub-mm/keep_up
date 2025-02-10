# ./scripts/build_calendar.py
import calendar


class CalendarBuild:
    day_to_num = {'MONDAY': 1, 'TUESDAY': 2, 'WEDNESDAY': 3, 'THURSDAY': 4, 'FRIDAY': 5, 'SATURDAY': 6, 'SUNDAY': 7}

    def __init__(self, mm, yy):
        self.mm = mm
        self.yy = yy
        self.first_day = calendar.monthrange(yy, mm)[0]
        self.num_of_days = calendar.monthrange(yy, mm)[1]
        self.month_layout = []

    def get_layout_month(self):
        weeks = calendar.monthcalendar(self.yy, self.mm)
        vertical_layout = list(map(list, zip(*weeks)))

        return vertical_layout

    def get_layout_year(self):
        vertical_layout = []
        for month in range(1, 13):
            weeks = calendar.monthcalendar(self.yy, month)
            vertical_layout.append(list(map(list, zip(*weeks))))

        return vertical_layout

    def get_month_name(self):
        num_to_month = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        return ''.join(key for key, val in num_to_month.items() if val == self.mm)

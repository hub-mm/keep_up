# ./scripts/build_habits.py
import uuid
import calendar
from datetime import datetime, timedelta


class HabitBuild:
    habit_list = {}

    def __init__(self, date, habit, frequency):
        day, month, year = date.split('/')
        self.day = int(day)
        self.month = int(month)
        self.year = int(year)
        self.habit = habit
        self.frequency = frequency
        self.id = uuid.uuid4()
        self.start_date = datetime(self.year, self.month, self.day)
        self.completed_dates = set()

    @classmethod
    def add_habit(cls, date, habit, frequency):
        day, month, year = date.split('/')
        day = int(day)
        month = int(month)
        year = int(year)

        freq_mapping = {
            'daily': 1,
            'alternate': 2,
            'tridum': 3,
            'weekly': 7,
            'monthly': calendar.monthrange(year, month)[1]
        }

        habit_instance = cls(date, habit, freq_mapping[frequency])
        cls.habit_list[habit_instance.id] = habit_instance

        return habit_instance

    @classmethod
    def get_habits_for_date(cls, date_str):
        day, month, year = date_str.split('/')
        selected_date = datetime(int(year), int(month), int(day))
        habits_for_day = []

        for habit in cls.habit_list.values():
            delta = (selected_date - habit.start_date).days

            if delta >= 0 and delta % habit.frequency == 0:
                habits_for_day.append(habit)

        return habits_for_day

    def mark_complete(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        except ValueError:
            print('Invalid date format.')
            return
        self.completed_dates.add(date_obj)

    def is_complete_for_date(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        except ValueError:
            return False
        return date_obj in self.completed_dates

    @classmethod
    def complete_habit_for_date(cls, habit_id_str, date_str):
        try:
            habit_id = uuid.UUID(habit_id_str)
        except ValueError:
            print('Invalid habit ID.')
            return None
        habit = cls.habit_list.get(habit_id)
        if habit:
            habit.mark_complete(date_str)
            return habit
        else:
            print('Habit not found.')
            return None

    @classmethod
    def delete_habit(cls, habit_id_str):
        try:
            habit_id = uuid.UUID(habit_id_str)
        except ValueError:
            print("Invalid habit ID.")
            return None

        if habit_id in cls.habit_list:
            del cls.habit_list[habit_id]
            return habit_id
        else:
            print('Habit not found.')
            return None
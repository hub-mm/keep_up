# ./scripts/build_habits.py
import uuid
import calendar
import json
import os
import atexit
from datetime import datetime


class HabitBuild:
    data_dir = 'json'
    data_file = os.path.join(data_dir, 'habits_data.json')

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

    def to_dict(self):
        return {
            'day': self.day,
            'month': self.month,
            'year': self.year,
            'habit': self.habit,
            'frequency': self.frequency,
            'id': str(self.id),
            'start_date': self.start_date.isoformat(),
            'completed_dates': [dt.isoformat() for dt in self.completed_dates],
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls.__new__(cls)
        obj.day = data['day']
        obj.month = data['month']
        obj.year = data['year']
        obj.habit = data['habit']
        obj.frequency = data['frequency']
        obj.id = uuid.UUID(data['id'])
        obj.start_date = datetime.fromisoformat(data['start_date'])
        obj.completed_dates = {datetime.fromisoformat(dt) for dt in data.get('completed_dates', [])}
        return obj

    @classmethod
    def load_data(cls):
        if not os.path.exists(cls.data_dir):
            os.makedirs(cls.data_dir)

        if os.path.exists(cls.data_file):
            try:
                with open(cls.data_file, 'r') as f:
                    data = json.load(f)
                cls.habit_list = {}
                for habit_data in data:
                    habit = cls.from_dict(habit_data)
                    cls.habit_list[habit.id] = habit
                print('Habits loaded successfully.')
            except Exception as e:
                print(f"Error loading habits data: {e}")

    @classmethod
    def save_data(cls):
        if not os.path.exists(cls.data_dir):
            os.makedirs(cls.data_dir)

        try:
            data = [habit.to_dict() for habit in cls.habit_list.values()]
            with open(cls.data_file, 'w') as f:
                json.dump(data, f)
            print('Habits saved successfully.')
        except Exception as e:
            print(f"Error saving habits data: {e}")

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


atexit.register(HabitBuild.save_data)
HabitBuild.load_data()

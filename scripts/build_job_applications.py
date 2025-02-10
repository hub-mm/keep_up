# ./scripts/job_application_trackers.py
import uuid
import json
import os
import atexit


class JobApplicationBuild:
    data_dir = 'json'
    data_file = os.path.join(data_dir, 'job_applications.json')

    job_list = {}

    def __init__(self, company=None, role=None, link=None, location=None, date=None):
        self.company = company
        self.role = role
        self.link = link
        self.location = location
        self.date = date
        self.id = uuid.uuid4()
        JobApplicationBuild.job_list[self.id] = {
            'company': self.company,
            'role': self.role,
            'link': self.link,
            'location': self.location,
            'date': self.date,
            'status': None
        }

    @classmethod
    def delete_job(cls, job_id):
        try:
            job_uuid = uuid.UUID(job_id)
        except ValueError:
            print('Invalid job_id format:', job_id)
            return
        if job_uuid in cls.job_list:
            del cls.job_list[job_uuid]
        else:
            print('Job id not found', job_uuid)

    @classmethod
    def add_status(cls, job_id, status):
        try:
            job_uuid = uuid.UUID(job_id)
        except ValueError:
            print('Invalid job_id format:', job_id)
            return
        if job_uuid in cls.job_list:
            cls.job_list[job_uuid]['status'] = status
        else:
            print('Job id not found', job_uuid)

    @classmethod
    def load_data(cls):
        if not os.path.exists(cls.data_dir):
            os.makedirs(cls.data_dir)

        if os.path.exists(cls.data_file):
            try:
                with open(cls.data_file, 'r') as f:
                    data = json.load(f)
                cls.job_list = {}

                for job_id_str, job_data in data.items():
                    cls.job_list[uuid.UUID(job_id_str)] = job_data
                print('Job applications loaded successfully.')
            except Exception as e:
                print(f"Error loading job applications: {e}")
        else:
            cls.job_list = {}

    @classmethod
    def save_data(cls):
        if not os.path.exists(cls.data_dir):
            os.makedirs(cls.data_dir)
        try:
            data_to_save = {str(job_id): job_data for job_id, job_data in cls.job_list.items()}
            with open(cls.data_file, 'w') as f:
                json.dump(data_to_save, f)
            print('Job applications saved successfully.')
        except Exception as e:
            print(f"Error saving job applications: {e}")


atexit.register(JobApplicationBuild.save_data)
JobApplicationBuild.load_data()

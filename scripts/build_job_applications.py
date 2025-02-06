# ./scripts/job_application_trackers.py
import uuid


class JobApplicationBuild:
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
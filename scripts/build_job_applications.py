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
            'date': self.date
        }
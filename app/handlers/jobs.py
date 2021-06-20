from datetime import datetime
from time import time as ttime

import tornado
from tornado.web import MissingArgumentError
import uuid

from config import SCHEDULED_CALLBACKS, SCHEDULED_JOBS, RUNNING_JOBS, DATE_FORMAT, JOB_HISTORY
from runner.jobs import schedule_job
from utils.utils import relative_date_to_timedelta


class JobsHandler(tornado.web.RequestHandler):
    def get(self):
        """
        tags:
        - jobs
        summary: List all jobs, them being in running state, scheduled or in the history
        produces:
        - application/json
        responses:
          200:
            description: list of jobs
        """
        jobs = {
            "running": RUNNING_JOBS,
            "scheduled": SCHEDULED_JOBS,
            "history": JOB_HISTORY
        }
        self.write(jobs)

class JobSchedulerHandler(tornado.web.RequestHandler):
    async def post(self):
        """
        tags:
        - jobs
        summary: Schedule a job at given time
        produces:
        - application/json
        responses:
          200:
            description: schedule a job
        """
        job_name = self.get_argument('job_name')
        random_id = uuid.uuid4().hex
        date, relative = '', ''
        try:
            if self.get_argument('time'):
                date = self.get_argument('time')
                relative = True
        except MissingArgumentError:
            date = self.get_argument('date')
            relative = False

        await schedule_job(job_name=job_name, scheduled_date=date, job_id=random_id, relative=relative)
        self.write({"message": f"job {job_name} with id {random_id} will be scheduled to run in {date}"})
    
class JobDetailHandler(tornado.web.RequestHandler):
    def get(self, job_id):
        if job_id in SCHEDULED_JOBS.keys():
            self.write(SCHEDULED_JOBS[job_id])
        elif job_id in RUNNING_JOBS.keys():
            self.write(RUNNING_JOBS[job_id])
        else:
            self.write(JOB_HISTORY[job_id])

    
    def delete(self, id):
        SCHEDULED_CALLBACKS[id].cancel()
        SCHEDULED_CALLBACKS.pop(id)
        deleted_job = SCHEDULED_JOBS.pop(id)
        JOB_HISTORY[id] = deleted_job
        JOB_HISTORY[id]['finish_status'] = 'did_not_run'
        JOB_HISTORY[id]['finish_date'] = datetime.fromtimestamp(ttime()).strftime(DATE_FORMAT)
        JOB_HISTORY[id]['status'] = 'canceled'
        self.write({"message": f"job {id} was de-scheduled"})

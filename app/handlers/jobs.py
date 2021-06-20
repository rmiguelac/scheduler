from datetime import datetime
from time import time as ttime

import tornado
import uuid

from config import SCHEDULED_CALLBACKS, SCHEDULED_JOBS, RUNNING_JOBS, DATE_FORMAT, JOB_HISTORY
from runner.jobs import schedule_job


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

    async def post(self):
        """
        tags:
        - jobs
        summary: Schedule
        """
        job_name = self.get_argument('job_name')
        date = self.get_argument('date')
        random_id = uuid.uuid4().hex
        await schedule_job(job_name=job_name, date=date, job_id=random_id)
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
        self.write({"message": f"job {id} was deleted"})

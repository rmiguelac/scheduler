from datetime import datetime
from functools import partial
from time import sleep, time as ttime

import tornado

from utils.utils import relative_date_to_timedelta
from config import SCHEDULED_CALLBACKS, SCHEDULED_JOBS, RUNNING_JOBS, DATE_FORMAT, JOB_HISTORY
from runner.docker_job import run_job

async def schedule_job(job_name: str, scheduled_date: str, job_id: str, relative: bool):
    now = datetime.fromtimestamp(ttime())
    if relative:
        run_time_timestamp = (now + relative_date_to_timedelta(scheduled_date)).timestamp()
        scheduled_to = (now + relative_date_to_timedelta(scheduled_date)).strftime(DATE_FORMAT)
    else:
        run_time_timestamp = datetime.strptime(scheduled_date, DATE_FORMAT).timestamp()
        scheduled_to = scheduled_date
    x = tornado.ioloop.IOLoop.instance().call_at(callback=runjob, job_id=job_id, job_name=job_name, when=run_time_timestamp)
    SCHEDULED_JOBS[job_id] = {
        "id": job_id,
        "job_name": job_name,
        "scheduled_in": now.strftime(DATE_FORMAT),
        "scheduled_to": scheduled_to,
        "status": "scheduled"
    }
    SCHEDULED_CALLBACKS[job_id] = x


def runjob(job_name: str, job_id: str):
    delayed_args = partial(docker_job, job_name, job_id)
    tornado.ioloop.IOLoop.instance().run_in_executor(None, delayed_args)

def docker_job(job_name: str, job_id: str):
    running_job = SCHEDULED_JOBS.pop(job_id)
    RUNNING_JOBS[job_id] = running_job
    RUNNING_JOBS[job_id]["status"] = "running"
    run_job(image=job_name)
    print(f"{job_name} ran...")
    ran_job = RUNNING_JOBS.pop(job_id)
    JOB_HISTORY[job_id] = ran_job
    JOB_HISTORY[job_id]['finish_status'] = 'success'
    JOB_HISTORY[job_id]['finish_date'] = datetime.fromtimestamp(ttime()).strftime(DATE_FORMAT)
    JOB_HISTORY[job_id]['status'] = 'finished'

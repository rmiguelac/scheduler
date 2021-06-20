from datetime import datetime, timedelta
from time import sleep, time as ttime
import uuid
import re
from functools import partial

import tornado.ioloop
import tornado.web


RUNNING_JOBS = {}
SCHEDULED_CALLBACKS = {}
JOB_HISTORY = {}
SCHEDULED_JOBS = {}
DATE_FORMAT = "%d-%m-%Y %H:%M:%S"

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/jobs')
        return

class JobsHandler(tornado.web.RequestHandler):
    def get(self):
        jobs = {
            "running": RUNNING_JOBS,
            "scheduled": SCHEDULED_JOBS,
            "history": JOB_HISTORY
        }
        self.write(jobs)

    async def post(self):
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


async def schedule_job(job_name: str, date: str, job_id: str):
    now = datetime.fromtimestamp(ttime())
    run_time_timestamp = (now + strdate_to_datetime(date)).timestamp()
    x = tornado.ioloop.IOLoop.instance().call_at(callback=runjob, job_id=job_id, job_name=job_name, when=run_time_timestamp)
    SCHEDULED_JOBS[job_id] = {
        "id": job_id,
        "job_name": job_name,
        "scheduled_in": now.strftime(DATE_FORMAT),
        "scheduled_to": (now + strdate_to_datetime(date)).strftime(DATE_FORMAT),
        "status": "scheduled"
    }
    SCHEDULED_CALLBACKS[job_id] = x


def runjob(job_name: str, job_id: str):
    delayed_args = partial(delayed, job_name, job_id)
    tornado.ioloop.IOLoop.instance().run_in_executor(None, delayed_args)

def delayed(job_name: str, job_id: str):
    running_job = SCHEDULED_JOBS.pop(job_id)
    RUNNING_JOBS[job_id] = running_job
    RUNNING_JOBS[job_id]["status"] = "running"
    sleep(5)
    print(f"{job_name} ran...")
    ran_job = RUNNING_JOBS.pop(job_id)
    JOB_HISTORY[job_id] = ran_job
    JOB_HISTORY[job_id]['finish_status'] = 'success'
    JOB_HISTORY[job_id]['finish_date'] = datetime.fromtimestamp(ttime()).strftime(DATE_FORMAT)
    JOB_HISTORY[job_id]['status'] = 'finished'

def strdate_to_datetime(date: str) -> timedelta:
    """
    handles absolute and relative dates and returns
    the datetime object with current time adding the
    given relative value
    """
    relative_pattern = re.compile('\d*[hms]{1}', re.IGNORECASE)
    if relative_pattern.match(date):
        delta = int(re.sub('[dhms]', '', date, re.IGNORECASE))
        if 'h' in date or 'H' in date:
            return timedelta(hours=delta)
        elif 'm' in date or 'M' in date:
            return timedelta(minutes=delta)
        elif 'd' in date or 'D' in date:
            return timedelta(days=delta)
        else:
            return timedelta(seconds=delta)


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/jobs", JobsHandler),
        (r"/job/(.*)", JobDetailHandler),
    ], debug=True)
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
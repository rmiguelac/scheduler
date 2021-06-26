import tornado.ioloop
import tornado.web

from handlers.jobs import JobDetailHandler, JobsHandler, JobSchedulerHandler
from handlers.main import MainHandler


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/jobs", JobsHandler),
        (r"/job", JobSchedulerHandler),
        (r"/job/(.*)", JobDetailHandler),
    ], debug=True)
    application.listen(8888)
    print("[INFO] Application started and port 8888 is listening")
    tornado.ioloop.IOLoop.current().start()
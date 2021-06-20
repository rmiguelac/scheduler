import tornado.ioloop
import tornado.web

from handlers.jobs import JobDetailHandler, JobsHandler
from handlers.main import MainHandler


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/jobs", JobsHandler),
        (r"/job/(.*)", JobDetailHandler),
    ], debug=True)
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
import tornado

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/jobs')
        return


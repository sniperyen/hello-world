# -.- coding:utf-8 -.-

import tornado.web
import tornado.gen
import tornado.ioloop
import tornado.options
import tornado.httpserver


# 其实是非堵塞模式，只不过每个连接要等5秒
class BlockingHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        # 如果这条命令没看懂的话，请参考这个链接: http://www.tornadoweb.org/en/stable/faq.html
        yield tornado.gen.sleep(5)
        res = {'code': 0, 'message': 'I am a message from blocking request!'}
        self.finish(res)
        # self.write('ok')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/blocking', BlockingHandler),
        ]
        super(Application, self).__init__(handlers)


if __name__ == "__main__":
    tornado.options.define("port", default=88, help="run on the given port", type=int)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()    

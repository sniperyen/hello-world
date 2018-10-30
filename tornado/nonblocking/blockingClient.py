# -.- coding:utf-8 -.-

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.websocket

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor  # 这个并发库在python3自带;在python2需要安装sudo pip install futures
import tornado.gen 
import tornado.httpclient # 采用tornado自带的异步httpclient客户端

import requests
import json
from functools import wraps

# 参考 
# https://my.oschina.net/zhengtong0898/blog/715615
# http://demo.pythoner.com/itt2zh/ch5.html

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/blocking', BlockHandler),
            ('/non_blocking1', NonBlockHandler1),
            ('/non_blocking2', NonBlockHandler2),
            ('/common', CommonHandler),  # 测试blocking或non_blocking被并发访问时，此url是否可以被访问  http://127.0.0.1/common
        ]
        super(Application, self).__init__(handlers)

        # 建议设定为CPU核心数量 * 4或8或16也是可以接受的, 取决于计算量，计算量越大设定的值应该越小.
        self.executor = ThreadPoolExecutor(16)



class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.blocking_url = "http://127.0.0.1:88/blocking"
    
    @property
    def executor(self):
        return self.application.executor

    def on_response(self, resp):
        if resp.code == 200:
            resp = json.loads(resp.body)
            self.write(json.dumps(resp, indent=4, separators=(',', ':')))
        else:
            resp = {"code": 1, "message": "error when fetch something"}
            self.write(json.dumps(resp, indent=4, separators=(',', ':')))
        self.finish()



# tornado.web.asynchronous,告诉Tornado保持连接开启
# 你必须在你的RequestHandler对象中调用finish方法来显式地告诉Tornado关闭连接。（否则，请求将可能挂起，浏览器可能不会显示我们已经发送给客户端的数据。）
class NonBlockHandler1(BaseHandler):

    @tornado.web.asynchronous
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient(max_clients=100)  # 默认情况下只允许同时发起10个客户端

        # 方式一：回调函数
        client.fetch(self.blocking_url, callback=self.on_response)

        # # 方式二：可以不使用上面的装饰器，原生写法
        # future = client.fetch(self.blocking_url, callback=self.on_response)        
        # tornado.ioloop.IOLoop.current().add_future(future)  # callback放这里也可以

        # # 方式三：可以不使用上面的装饰器，使用 tornado.concurrent.futures
        # future = tornado.concurrent.Future()
        # fetch_future = client.fetch(self.blocking_url, callback=self.on_response)
        # fetch_future.add_done_callback(lambda x: future.set_result(x.result())


# tornado.gen.coroutine + ThreadPool/ProcessPool
class NonBlockHandler2(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        # 方式一：使用异步方式
        client = tornado.httpclient.AsyncHTTPClient(max_clients=100)
        resp = yield tornado.gen.Task(client.fetch, (self.blocking_url))  
        # Task利用了yield，它的隐藏方法run()利用了gen.send()方法， 这种构建的美在于它在请求处理程序中返回HTTP响应，而不是回调函数中

        # # 方式二：使用同步方式，但依旧是非堵塞的
        # resp = yield self.executor.submit(requests.get, (self.blocking_url))

        self.on_response(resp)

        # 注：tornado的异步库只针对httpclient, 没有针对mysql或者其他数据库的异步库(自己写一个异步库难度太高，因为辗转十几个源码文件的重度调用以及每个类中的状态控制)。
        # coroutine结合threadpool让编写异步代码不再拆成多个函数，变量能够共享，堵塞的代码（例如 requests、mysql.connect、密集计算）可以不影响ioloop，形成真正的闭合.


class BlockHandler(BaseHandler):

    def get(self, *args, **kwargs):
        resp = requests.get(self.blocking_url)     # blocked here.
        self.write(resp.content)


class CommonHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.write('I can access the page. So the web server is not blocked.')


class EchoHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message('connected!')

    def on_message(self, message): 
        self.write_message(message)
        self.close()

    def on_close(self):
        pass

# # region 定时任务
# def sync_loop_call(delta=60 * 1000):
#     """
#     Wait for func down then process add_timeout
#     """
#     def wrap_loop(func):
#         @wraps(func)
#         @tornado.gen.coroutine
#         def wrap_func(*args, **kwargs):
#             options.logger.info("function %r start at %d" %
#                                 (func.__name__, int(time.time())))
#             try:
#                 yield func(*args, **kwargs)
#             except Exception, e:
#                 options.logger.error("function %r error: %s" %
#                                      (func.__name__, e))
#             options.logger.info("function %r end at %d" %
#                                 (func.__name__, int(time.time())))
#             tornado.ioloop.IOLoop.instance().add_timeout(
#                 datetime.timedelta(milliseconds=delta),
#                 wrap_func)
#         return wrap_func
#     return wrap_loop


# @sync_loop_call(delta=10 * 1000)
# def worker():
#     """
#     Do something
#     """
#     pass
# # endregion




# siege http://127.0.0.1/non_blocking1 -c10 -t60s

if __name__ == "__main__":
    tornado.options.define("port", default=80, help="run on the given port", type=int)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()

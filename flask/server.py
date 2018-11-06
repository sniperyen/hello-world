import BaseHTTPServer
import os
import socket

class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/hchan.jpg":
            hostname = socket.gethostname()
            message_parts = [
                "<html>",
                "<head><title>Hello World</title></head>",
                "<body style=\"text-align:center;\">",
                "<p><img src='hchan.jpg' /></p>",
                "<h3>Hello Alauda!</h3><br />",
                "<p>My hostname is <b>" + hostname + "</b></p>",
                "</body>",
                "<html>"
            ]
            message = '\r\n'.join(message_parts)
            print message
            # message = "New request arrived from %s:%d" % self.client_address
            self.send_response(200)
            self.end_headers()
            self.wfile.write(message)
        else:
            f = open(os.curdir + os.sep + self.path)
            self.send_response(200)
            self.send_header('Content-type', 'image/jpg')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()


if __name__ == '__main__':
    print "Server started, Listening on port 80"
    server = BaseHTTPServer.HTTPServer(('0.0.0.0', 80), WebRequestHandler)
    server.serve_forever()
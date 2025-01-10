from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

PORT = 8080

class CustomHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        with open("/var/log/simple_http_server.log", "a") as log_file:
            log_file.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))

with TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()

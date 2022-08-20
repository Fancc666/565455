from http.server import BaseHTTPRequestHandler
import requests


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        req = requests.get("https://baidu.com/")
        req.encoding = "utf-8"
        self.wfile.write(str(req.text).encode())
        return

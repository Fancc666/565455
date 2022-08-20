from http.server import BaseHTTPRequestHandler
import requests


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        req = requests.get("http://bilibili.com/")
        req.encoding = "UTF-8"
        self.wfile.write(str(req.text).encode('utf-8'))
        return

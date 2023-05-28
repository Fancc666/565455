# 重定向到github

from http.server import BaseHTTPRequestHandler
# from http.server import HTTPServer
import requests
import re
import json
from urllib.parse import unquote
import urllib3


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        urllib3.disable_warnings()
        self.send_response(302)
        self.send_header('Location', "https://github.com/Fancc666/565455")
        self.end_headers()
        self.end_with_none()

        return
    def show_text(self, text):
        self.wfile.write(str(text).encode('utf-8'))
    def get_para(self, name):
        f = re.findall(r"(?:\&|\?)"+name+r"=(.*?)(?:\&|$)", self.path)
        if len(f) > 0:
            return f[0]
        else:
            return ""
    def get_html(self, url):
        req = requests.get(url, verify=False)
        req.encoding = "utf-8"
        return req.text
    def err(self, msg):
        self.reply['code'] = 1
        self.reply['msg'] = msg
    def end(self):
        self.show_text("api_response=")
        self.show_text(json.dumps(self.reply))
    def end_with_none():
        pass


# if __name__ == "__main__":
#     s = HTTPServer(('localhost', 8888), handler)# localhost
#     print("server is running...")
#     s.serve_forever()

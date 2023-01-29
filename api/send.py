from http.server import BaseHTTPRequestHandler
# from http.server import HTTPServer
import requests
import re
import json
from urllib.parse import unquote
import urllib3


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        urllib3.disable_warnings()

        self.headers = {
            'Accept-Encoding': '',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }
        self.reply = {
            'code': 0,
            'msg': ""
        }

        link = self.get_para("link")
        link = unquote(link, 'utf-8')
        
        self.send_header('Access-Control-Allow-Origin', '*')
        
        if link!="":
            try:
                response = requests.get(link, headers=self.headers)
                ct = response.headers["Content-Type"]
                self.send_header('Content-type', ct)
                self.end_headers()
                self.wfile.write(response.content)
                return
            except Exception as e:
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.err("access is invalid/unknown content-type")
                self.end()
                return
        else:
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.err("paramter is missing")
            self.end()

        return
    def show_text(self, text):
        self.wfile.write(str(text).encode('utf-8'))
    def get_para(self, name):
        f = re.findall(r"(?:\&|\?)"+name+r"=(.*?)(?:$)", self.path)
        if len(f) > 0:
            return f[0]
        else:
            return ""
    def get_html(self, url):
        req = requests.get(url, verify=False, headers=self.headers)
        req.encoding = "utf-8"
        return req.text
    def err(self, msg):
        self.reply['code'] = 1
        self.reply['msg'] = msg
    def end(self):
        self.show_text("api_response=")
        self.show_text(json.dumps(self.reply))


# if __name__ == "__main__":
#     s = HTTPServer(('localhost', 8888), handler)
#     print("server is running...")
#     s.serve_forever()

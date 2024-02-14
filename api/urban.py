# 传输urbandic的内容
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import requests
import re
import json
from urllib.parse import unquote
import urllib3
from bs4 import BeautifulSoup

class handler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        "javascript or json"
        self.response_type = "javascript"
        super(handler, self).__init__(request, client_address, server)
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', f'text/{self.response_type}')
        self.end_headers()
        urllib3.disable_warnings()

        self.reply = {
            'code': 0,
            'msg': '',
            'data': []
        }

        search_word = self.get_para("s")
        if search_word != "":
            try:
                response = self.get_html(f"https://www.urbandictionary.com/define.php?term={search_word}")
                nodes = BeautifulSoup(response, "lxml")
                defs = nodes.find_all("div", class_="definition")
                self.reply["data"] = list(map(lambda x: str(x), defs))
            except Exception as e:
                self.err(str(e))
        else:
            self.err("Parameter Missing!")
        self.end()

    # def do_POST(self):
    #     self.send_response(200)
    #     self.send_header('Content-type', 'text/html')
    #     self.send_header('Access-Control-Allow-Origin', '*')
    #     self.end_headers()
    #     urllib3.disable_warnings()

    #     self.reply = {
    #         'code': 0,
    #         'msg': "",
    #         'title': ""
    #     }

    #     return
    def show_text(self, text):
        self.wfile.write(str(text).encode('utf-8'))
    def get_para(self, name):
        f = re.findall(r"(?:\&|\?)"+name+r"=(.*?)(?:\&|$)", self.path)
        if len(f) > 0:
            return f[0]
        else:
            return ""
    def get_html(self, url, encode="utf-8"):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        req = requests.get(url, headers=headers, verify=False)
        req.encoding = encode
        return req.text
    def err(self, msg):
        self.reply['code'] = 1
        self.reply['msg'] = msg
    def end(self):
        if self.response_type == "javascript":
            self.show_text("api_response=")
        self.show_text(json.dumps(self.reply))


# if __name__ == "__main__":
#     s = HTTPServer(('127.0.0.1', 8888), handler)
#     print("server is running...")
#     s.serve_forever()

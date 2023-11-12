from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import re
import json
from urllib.parse import unquote, quote
import urllib3

class GWD:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.cookie = "Hm_lvt_9007fab6814e892d3020a64454da5a55=169975427=2; login=flase; ticketStr=201583372%7cgQHe7zwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAyeHRXOFJJbGVkN2kxb1YtVE5CMVUAAgQ5MVBlAwQAjScA; ASP.NET_SessionId=t5pb5u30gkzeqji22ig32giq; codeyzgswso=85d38c0278c0fb7f; gsw2017user=5168703%7c6A5471B38CFFFF27880E4F7E9679CF7Adaac0c43%7c2000%2f1%2f1; login=flase; wxopenid=oVc5H0qwnh6rNv6IynEDqtFIeuhc; Hm_lpvt_9007fab6814e892d3020a64454da5a55=1699754357"
        self.url = "https://so.gushiwen.cn/dict/fancha.aspx"
        self.response = None

    def cookie_seperator(self, cookie_text):
        groups = cookie_text.split(";")
        groups = map(lambda x: x.replace(" ", ""), groups)
        cookie_dict = {}
        for group in groups:
            key, val = re.findall(r"(.+?)\=(.+)", group)[0]
            cookie_dict[key] = val
        return cookie_dict

    def send_request(self, char):
        char = quote(char)
        para = f"z={char}&url=so.gushiwen.cn%2Fshiwenv_573d6514abc4.aspx"
        response = requests.post(self.url, data=para, headers=self.headers, cookies=self.cookie_seperator(self.cookie))
        response.encoding = "utf-8"
        self.response = response

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        urllib3.disable_warnings()

        self.reply = {
            'code': 0,
            'msg': ""
        }

        l = self.get_para("c")
        t = self.get_para("type")
        if t == "":
            self.resp_type = "json"
        else:
            self.resp_type = "api"
        if l != "":
            l = unquote(l, 'utf-8')
            try:
                g = GWD()
                g.send_request(l)
                self.show_text(g.response.text)
            except Exception as e:
                self.err("access is invalid")
                self.end()
        else:
            self.err("parameter is missing")
            self.end()

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
        if self.resp_type == "api":
            self.show_text("api_response=")
        else:
            pass
        self.show_text(json.dumps(self.reply))


# if __name__ == "__main__":
#     s = HTTPServer(('localhost', 8888), handler)
#     print("server is running...")
#     s.serve_forever()

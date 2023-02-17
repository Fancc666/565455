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
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        urllib3.disable_warnings()

        self.reply = {
            'code': 0,
            'msg': "",
            'mima': ""
        }

        route = self.get_para("route")

        route = unquote(route, 'utf-8')

        if route != "":
            url = "https://nc.cli.im/qrcoderoute/qrcodeRouteNew"
            data = {
                "qrcode_route": route,
                "password": "",
                "render_default_fields": "0",
                "render_edit_btn": "1"
            }
            try:
                response = requests.post(url, data=data)
            except Exception as e:
                self.err("access is denied")
                self.end()
                return
            response.encoding = "utf-8"
            try:
                res_js = json.loads(response.text)
                mmline = res_js['data']['qrcode_msg']['qrcode_record']['list_name']
                mm = re.findall(r"（密码：(.*?)）", mmline)[0]
                self.reply["mima"] = mm
                self.end()
            except Exception as e:
                self.err("password is not found")
                self.end()
                return
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
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) \
                        AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            "referer": "https://m.bilibili.com/"
        }
        req = requests.get(url, verify=False, headers=headers)
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

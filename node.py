# 用不变的链接导入nodefree节点-clash

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import requests
import re
import json
from urllib.parse import unquote
import urllib3


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # self.send_header('Content-type', 'text/html')
        urllib3.disable_warnings()
        self.reply = {
            'code': 0,
            'msg': ""
        }

        # 得到最新链接，并使用使用header返回
        try:
            home_html = self.get_html("https://nodefree.org/")
            latest_link_block = re.findall(r"<a class=\"item-img-inner\" href=\"(https://nodefree\.org/p/.+?)\"", home_html)[0]
            latest_link_html = self.get_html(latest_link_block)
            latest_link = re.findall(r"<p>(https://nodefree\.org/dy/.+?\.yaml)</p>", latest_link_html)[0]
            self.send_response(302)
            self.send_header('Location', latest_link)
            self.end_headers()
            self.end_with_none()
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.err("unexpected error: "+str(e))
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
        self.show_text("api_response=")
        self.show_text(json.dumps(self.reply))
    def end_with_none():
        pass


if __name__ == "__main__":
    s = HTTPServer(('192.168.18.8', 8888), handler)# localhost
    print("server is running...")
    s.serve_forever()

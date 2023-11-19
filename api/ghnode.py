# 用不变的链接导入clashgithub节点-clash

from http.server import BaseHTTPRequestHandler
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

        try:
            home_html = self.get_html("https://clashgithub.com/")
            latest_link_block = re.findall(r"<a href=\"(http.*?)\" title=\"", home_html)[0]
            latest_link_html = self.get_html(latest_link_block)
            latest_link = re.findall(r"<p>(https://clashgithub\.com/wp-content/uploads/rss/.*\.yml)</p>", latest_link_html)[0]
            link_text = self.get_html(latest_link)
            # self.send_response(302)
            # self.send_header('Location', latest_link)
            # self.end_headers()
            self.send_response(200)
            self.send_header('Content-type', 'text/yml; charset=utf-8')
            self.end_headers()
            # wash
            text_lines = link_text.split("\n")
            op = ""
            for line in text_lines:
                if "fake-ip-filter:" in line:
                    continue
                op += line
                op += "\n"
            self.show_text(op)
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


# if __name__ == "__main__":
#     s = HTTPServer(('localhost', 8888), handler)# localhost
#     print("server is running...")
#     s.serve_forever()

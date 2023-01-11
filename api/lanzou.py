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

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "referer": "https://lanzou.com/",
            "Accept-Encoding":"gzip, deflate, lzma, sdch", # 重点1
            "Accept-Language":"zh-CN,zh;q=0.8", # 重点2    
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"# 重点3
        }

        self.reply = {
            'code': 0,
            'msg': "",
            'link': ""
        }

        lz = self.get_para("lz")
        lz = unquote(lz, 'utf-8')

        if lz != "":
            try:
                # 1.用户链
                user_page_url = lz
                user_page_text = self.get_html(user_page_url)

                # 2.button-page
                button_page_url = re.findall(r"[^-]<iframe (?:.*?) src=\"(.*?)\" (?:.*?)></iframe>", user_page_text)[0]
                button_page_url = "https://lanzout.com" + button_page_url
                button_page_text = self.get_html(button_page_url)

                # 3.action
                sign = re.findall(r"'sign':'(.*?)'", button_page_text)[0]
                response_sign = requests.post("https://lanzout.com/ajaxm.php", headers=self.headers, 
                    data={
                        "action": "downprocess",
                        "signs": "%3Fctdf",
                        "websign": "",
                        "websignkey": "iZVZ",
                        "ves": 1,
                        "sign": sign
                    }
                )
                information = json.loads(response_sign.text)

                # 4.end
                para = information["url"]
                file_url = "https://developer.lanzoug.com/file/"+para
                self.reply["link"] = file_url
                self.end()
                return
            except Exception as e:
                self.err("access is invalid")
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

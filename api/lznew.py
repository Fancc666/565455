from http.server import BaseHTTPRequestHandler
# from http.server import HTTPServer
import requests
import re
import json
from urllib.parse import unquote, urlencode
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
        self.post_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "referer": "https://lanzou.com/",
            "Accept-Encoding":"gzip, deflate, lzma, sdch", # 重点1
            "Accept-Language":"zh-CN,zh;q=0.8", # 重点2    
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",# 重点3
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" # 重点4
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
                # 2.1处理文本
                properties = self.analyze(button_page_text)

                # 3.action
                response_sign = requests.post(f"https://lanzout.com/ajaxm.php{properties['url']}", headers=self.post_headers, 
                    data=properties["para"]
                )
                information = json.loads(response_sign.text)

                # 4.end
                if "dom" in information and "url" in information:
                    file_url = f"{information['dom']}/file/{information['url']}"
                    self.reply["link"] = file_url
                    self.end()
                    return
                else:
                    raise(Exception("No key error."))
            except Exception as e:
                self.err("access is invalid")
                self.end()
                return
        else:
            self.err("parameter is missing")
            self.end()

        return
    def analyze(self, text):
        reg = r"var (.+) = '(.*)';"
        matches = re.findall(reg, text)
        properties = {}
        for key, val in matches:
            properties[key] = val
        contents = {
            'action':'downprocess',
            'signs':properties["ajaxdata"],
            'websignkey':'Us3Z',
            'sign':properties["wp_sign"],
            'websign':properties["v3v3"],
            'kd':1,
            'ves':1 
        }
        reg2 = r"\?file=\d+"
        url_match = re.findall(reg2, text)
        result = {
            "para": urlencode(contents),
            "url": url_match[len(url_match)-1]
        }
        return result
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
    def get_head(self, url):
        req = requests.get(url, verify=False, headers=self.headers)
        req.encoding = "utf-8"
        return req.url
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

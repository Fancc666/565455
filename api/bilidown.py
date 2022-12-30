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
            'v_link': ""
        }

        bv_num = self.get_para("bv")
        p_num = self.get_para("p")

        bv_num = unquote(bv_num, 'utf-8')
        p_num = unquote(p_num, 'utf-8')
        if bv_num != "" and p_num != "" and p_num.isnumeric():
            try:
                p_num = int(p_num)
                # 获取AID
                cid_html = self.get_html("https://api.bilibili.com/x/web-interface/view/detail?aid=&bvid="+bv_num[3:]+"&recommend_type=&need_rcmd_reason=1")
                cid_json = json.loads(cid_html)
                try:
                    aid = cid_json["data"]["View"]["aid"]
                    # 获取CID
                    pages = cid_json["data"]["View"]["pages"]
                    if (len(pages) >= p_num and p_num > 0):
                        cid = cid_json["data"]["View"]["pages"][p_num - 1]["cid"]
                    else:
                        cid = cid_json["data"]["View"]["cid"]
                except Exception as e:
                    self.err("aid/cid is error")
                    self.end()
                    return
                # 获取视频链接
                video_url = "https://api.bilibili.com/x/player/playurl?cid="+str(cid)+"&avid="+str(aid)+"&platform=html5&otype=json&qn=16&type=mp4&html5=1"
                video_html = self.get_html(video_url)
                video_json = json.loads(video_html)
                try:
                    video_link = video_json["data"]["durl"][0]["url"]
                except Exception as e:
                    self.err("can not find video link")
                    self.end()
                    return
                video_link_r = "https://upos-sz-mirrorcos.bilivideo.com/"+"/".join(video_link.split("/")[3:])
                self.reply["msg"] = "ok"
                self.reply["v_link"] = video_link_r
                self.end()
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

from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'texxt/plain')
        self.end_headers()
        self.wfile.write("hello world! vercel".encode())
        return

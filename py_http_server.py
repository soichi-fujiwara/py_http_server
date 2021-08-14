import os
import sys
import urllib.parse
import html
import json

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from http import HTTPStatus
from urllib.parse import parse_qs, urlparse

PORT = 8000

class StubHttpRequestHandler(BaseHTTPRequestHandler):
    server_version = "HTTP Stub/0.1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # 呼び出し方
        # ブラウザで「http://localhost:8000」にアクセス
        enc = sys.getfilesystemencoding()
        title = "HTTP Stub"

        r = []
        r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                 '"http://www.w3.org/TR/html4/strict.dtd">')
        r.append('<html>\n<head>')
        r.append('<meta http-equiv="Content-Type" '
                 'content="text/html; charset=%s">' % enc)
        r.append('<title>%s</title>\n</head>' % title)
        r.append('<body>\n<h1>%s</h1>' % title)
        r.append('<hr>\n<ul>')
        r.append("Stub Opened.")
        r.append('</ul>\n<hr>\n</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()

        self.wfile.write(encoded)     

    def do_POST(self):
        # 呼び出し方(PowerShell)
        # Invoke-WebRequest -Method Post http://localhost:8000 -body @{param1 = "abc";param2 = "xyz"}
        enc = sys.getfilesystemencoding()
        print("="*50)

        length = self.headers.get('content-length')
        nbytes = int(length)
        rawPostData = self.rfile.read(nbytes)
        decodedPostData = rawPostData.decode(enc)
        postData = urllib.parse.parse_qs(decodedPostData)
        print(postData)

        self.send_response(HTTPStatus.OK)
        # self.send_header("Content-type", "text/plain; charset=utf-8")
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()

        # RESPONSE
        # 1. text/plain
        # self.wfile.write(postData["param1"][0].encode(encoding='utf-8'))

        # 2. application/json
        responseText = json.dumps({"a":1}) 
        self.wfile.write(responseText.encode(encoding='utf-8'))

handler = StubHttpRequestHandler
httpd = HTTPServer(('',PORT),handler)
httpd.serve_forever()
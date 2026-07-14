import http.server
import socketserver
import json
import os

PORT = 8000
DIRECTORY = "captures"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # capturesフォルダの中身を公開する設定
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # ブラウザから画像リストの要求があった場合の処理
        if self.path == '/api/files':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # capturesフォルダ内の .jpg を新しい順に並べて返す
            files = [f for f in os.listdir(DIRECTORY) if f.endswith('.jpg')]
            files.sort(reverse=True)
            self.wfile.write(json.dumps(files).encode())
        else:
            # それ以外（画像やHTML）は通常通り返す
            super().do_GET()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"🌐 UIサーバー起動: http://<ラズパイのIPアドレス>:{PORT}")
        print("停止するには Ctrl+C を押してください")
        httpd.serve_forever()

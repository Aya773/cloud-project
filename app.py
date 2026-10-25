from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", "5")
            self.end_headers()
            self.wfile.write(b"hello")
        except (BrokenPipeError, ConnectionResetError):
            pass
    def log_message(self, *args):
        pass

class Server(ThreadingHTTPServer):
    request_queue_size = 128
    daemon_threads = True

Server(("0.0.0.0", 8000), Handler).serve_forever()

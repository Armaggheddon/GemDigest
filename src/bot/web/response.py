from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

def run_http_server():
    """Starts an HTTP server that listens on port 8080."""
    PORT = 8080

    class MyHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            # Send 200 OK response
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Hello, this is a 200 OK response.")

    with TCPServer(("", PORT), MyHandler) as httpd:
        # print(f"Serving on port {PORT}")
        httpd.serve_forever()
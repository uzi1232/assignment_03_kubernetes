import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/isAlive":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"true")
        else:
            response = f"{self.path} not found."
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='HTTP probe server',
                    description='Serves probe endpoint for COMP 4016 assignment')
    parser.add_argument('-H', '--host', required=True, type=str)
    parser.add_argument('-p', '--port', required=True, type=int)
    args = parser.parse_args()
    server = HTTPServer((args.host, args.port), HttpHandler)
    server.serve_forever()

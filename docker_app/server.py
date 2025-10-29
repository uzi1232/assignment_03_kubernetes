import argparse
import json
import math
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from file_helper import write_to_file, get_file_content

file_path = "/data/value.txt"

def get_json(message):
    try:
        return json.loads(message)
    except Exception as exp:
        return None

def cpu_intensive_task(minutes):
    duration = minutes * 60
    end_time = time.time() + duration
    while time.time() < end_time:
        math.factorial(5000)
    print("Done CPU intensive task")

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/foo":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"bar")
        elif self.path == "/getString":
            value = get_file_content(file_path)
            if value is not None:
                self.send_response(200)
            else:
                self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(value.encode("utf-8"))       
        elif self.path == "/busywait":
            value = "Start wating for the response..."
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(value.encode("utf-8"))
            cpu_intensive_task(3)
        else:
            response = f"{self.path} not found."
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))

    def do_POST(self):
        if self.path == "/saveString":
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length)
            print("Received POST data:", request_body.decode())
            request = get_json(request_body.decode())
            if request is not None:
                if ("data" in request):
                    response = write_to_file(file_path, request.get("data"))
                    self.send_response(200)
                else:
                    response = f"Key 'data' not found"
                    self.send_response(404)
            else:
                response = f"Request JSON could not be parsed."
                self.send_response(400)

            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='HTTP server',
                    description='Serves different endpoints for COMP 4016 assignments')
    parser.add_argument('-H', '--host', required=True, type=str)
    parser.add_argument('-p', '--port', required=True, type=int)
    parser.add_argument('-c', '--config_env', type=str, default="CONFIG_PATH")
    args = parser.parse_args()
    config_path_env = args.config_env
    server = HTTPServer((args.host, args.port), HttpHandler)
    server.serve_forever()

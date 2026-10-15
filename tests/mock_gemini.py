"""Deterministic local Gemini protocol fixture. Never contacts Google."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/generate":
            self.send_error(404)
            return
        if self.headers.get("x-goog-api-key") != "integration-test-key":
            self.send_error(401)
            return
        size = int(self.headers.get("Content-Length", "0"))
        if size <= 0 or size > 32768:
            self.send_error(413)
            return
        try:
            payload = json.loads(self.rfile.read(size))
            assert "contents" in payload
            assert "parts" in payload["contents"][0]
            assert "text" in payload["contents"][0]["parts"][0]
        except (ValueError, KeyError, IndexError, AssertionError, TypeError):
            self.send_error(400)
            return
        action = json.dumps({"tool_name":"sum_numbers", "arguments":{"a":5,"b":10}})
        response = json.dumps({"candidates":[{"content":{"parts":[{"text":action}]}}]}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, _format, *_args):
        pass

if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 18763), Handler).serve_forever()

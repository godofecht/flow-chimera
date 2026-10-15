"""Deterministic Ollama /api/embed protocol test server, no model dependency."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/health":
            self.send_error(404)
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def do_POST(self):
        if self.path != "/api/embed":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        if length < 1 or length > 16384:
            self.send_error(413)
            return
        try:
            request = json.loads(self.rfile.read(length))
        except (ValueError, TypeError):
            self.send_error(400)
            return
        if request.get("model") != "qwen3-embedding:0.6b":
            self.send_error(400)
            return
        prompt = request.get("input")
        if not isinstance(prompt, str) or not prompt:
            self.send_error(400)
            return
        if "cat" in prompt.lower():
            vector = [0.9, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        elif "dog" in prompt.lower():
            vector = [0.1, 0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        else:
            vector = [0.25, -0.5, 0.75, 0.1, 0.0, 0.0, 0.0, 0.0]
        body = json.dumps({"model": request["model"], "embeddings": [vector], "total_duration": 123456}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, _format, *_args):
        pass

if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 18764), Handler).serve_forever()

import json
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer

class MockServerHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/api/shopping-cart":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')

            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "Invalid JSON format"
                }).encode('utf-8'))
                return

            if "items" not in data:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "Missing 'items' field in request"
                }).encode('utf-8'))
                return

            order_uuid = str(uuid.uuid4())

            response = {
                "success": True,
                "message": "Shopping list created successfully",
                "order_uuid": order_uuid,
                "items": data["items"]
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()

def run_mock_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, MockServerHandler)
    print("Mock server running on port 8080...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_mock_server()

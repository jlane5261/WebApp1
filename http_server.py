import http.server
import json

class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, route, handler):
        self.routes[route] = handler

    def route_request(self, path):
        if path in self.routes:
            return self.routes[path]
        else:
            return None

class BasicRequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.router = server.router
        super().__init__(request, client_address, server)

    def do_GET(self):
        handler = self.router.route_request(self.path)
        if handler:
            data = handler()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_error(404)

class WebFramework:
    def __init__(self, host, port):
        self.router = Router()
        self.server = http.server.HTTPServer((host, port), BasicRequestHandler)

    def add_route(self, route, handler):
        self.router.add_route(route, handler)

    def start(self):
        self.server.serve_forever()

# Example usage:
app = WebFramework('localhost', 8000)

def hello_world():
    return {'message': 'Hello, world!'}

app.add_route('/hello', hello_world)

app.start()
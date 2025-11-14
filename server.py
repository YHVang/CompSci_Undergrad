import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# Get folder where this file lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def server(path):
    """Return HTML content based on the requested path."""
    # Map URLs to files
    if path == '/':
        filename = 'index.html'
    elif path == '/about':
        filename = 'about.html'
    else:
        # Unknown path → simple 404
        return f"<h1>404 Not Found</h1><p>The page {path} does not exist.</p>"

    # Build full file path
    file_path = os.path.join(BASE_DIR, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()  # return HTML content as string
    except FileNotFoundError:
        return f"<h1>404 Not Found</h1><p>File {filename} not found.</p>"

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Call server() to get content
        message = server(self.path)

        # Convert string to bytes
        if isinstance(message, str):
            message = message.encode('utf-8')

        # Prepare headers
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        # Send the response
        self.wfile.write(message)

def run(port=8000):
    httpd = HTTPServer(('', port), SimpleHandler)
    print(f"Serving on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()

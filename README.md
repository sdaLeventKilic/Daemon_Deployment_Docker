# Simple HTTP Server with systemd and Docker
This repository demonstrates how to containerize and deploy a Python HTTP server using Docker,
along with a reverse proxy for load balancing and high availability.
## Features
- Containerized Python HTTP server running on port 8080.
- Managed using Docker and Docker Compose.
- Integrated reverse proxy (NGINX) for load balancing.
- High availability with at least 2 replicas.
- Logs output to a container volume.
---
## File Structure
```
.
├── Dockerfile
├── docker-compose.yml
├── app/
│ └── simple_http_server.py
├── reverse-proxy/
│ └── nginx.conf
└── README.md
```
---
## Application Code
The server is implemented in Python.
### **`app/simple_http_server.py`**
```python
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
PORT = 8080
class CustomHandler(SimpleHTTPRequestHandler):
def log_message(self, format, *args):
with open("/var/log/simple_http_server.log", "a") as log_file:
args))
log_file.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format %
with TCPServer(("", PORT), CustomHandler) as httpd:
print(f"Serving on port {PORT}")
httpd.serve_forever()
```
---
## Dockerfile
The Dockerfile creates an image for the Python HTTP server.
### **`Dockerfile`**
```dockerfile
# Use Python base image
FROM python:3.9-slim
# Set working directory
WORKDIR /usr/src/app
# Copy application code to container
COPY app/simple_http_server.py ./
# Create log directory
RUN mkdir -p /var/log && touch /var/log/simple_http_server.log
# Expose the application port
EXPOSE 8080
# Start the server
CMD ["python3", "simple_http_server.py"]
```
---
## Reverse Proxy Configuration
The reverse proxy (NGINX) balances requests between replicas.
### **`reverse-proxy/nginx.conf`**
```nginx
events {}
http {
upstream backend {
server app1:8080;
server app2:8080;
}
server {
listen 80;
}
```
---
location / {
proxy_pass http://backend;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
}
}
## Docker Compose Configuration
The `docker-compose.yml` file defines the application and reverse proxy services.
### **`docker-compose.yml`**
```yaml
version: "3.9"
services:
app:
build:
context: .
dockerfile: Dockerfile
deploy:
replicas: 2
restart_policy:
condition: on-failure
ports:
- "8080"
volumes:
- app-logs:/var/log
reverse-proxy:
image: nginx:latest
volumes:
- ./reverse-proxy/nginx.conf:/etc/nginx/nginx.conf:ro
ports:
- "80:80"
depends_on:
- app
volumes:
app-logs:
```
---
## Deployment Instructions
### 1. **Build and Start Services**
Run the following command to build the images and start the services:
```bash
docker-compose up --build -d
```
### 2. **Verify Running Containers**
Check the status of the services:
```bash
docker-compose ps
```
### 3. **Access the Application**
Open a browser or use `curl` to test the application:
```bash
curl http://localhost
```
### 4. **View Logs**
Access logs from the application container:
```bash
docker-compose logs app
```
---
## Summary
### Key Components
- **Application Script**: `app/simple_http_server.py`
- **Dockerfile**: Builds the Python HTTP server image.
- **Reverse Proxy**: Balances traffic between replicas.
- **Docker Compose**: Manages services and scaling.

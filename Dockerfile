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

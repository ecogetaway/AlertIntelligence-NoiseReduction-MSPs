#!/bin/bash

# Quick demo startup - finds available port automatically
PORT=$(python3 -c "
import socket
s = socket.socket()
s.bind(('', 0))
port = s.getsockname()[1]
s.close()
print(port)
")

echo "🚀 Starting MSP Alert Intelligence Demo on port $PORT"
echo "📍 Open: http://localhost:$PORT/frontend-demo.html"
echo "Press Ctrl+C to stop"
python3 -m http.server $PORT

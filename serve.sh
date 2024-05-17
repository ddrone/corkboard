#!/usr/bin/env bash

PORT=5000

# Experimentally, 200ms is enough for Flask server to start
# Worst case scenario, one would just have to F5 in the browser window.
sleep .2 && xdg-open http://localhost:$PORT/ &

FLASK_APP=server flask run --port $PORT

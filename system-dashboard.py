#!/usr/bin/env python3

from flask import Flask, jsonify, render_template_string
import os
import platform
import socket
from datetime import datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>System Dashboard</title>
    <style>
        body{
            font-family:Arial;
            background:#eef4ff;
            padding:40px;
        }
        .card{
            max-width:700px;
            margin:auto;
            background:white;
            padding:30px;
            border-radius:12px;
            box-shadow:0 8px 20px rgba(0,0,0,.15);
        }
        h1{
            color:#2457d6;
        }
        table{
            width:100%;
            border-collapse:collapse;
            margin-top:20px;
        }
        td{
            padding:12px;
            border-bottom:1px solid #ddd;
        }
        .badge{
            display:inline-block;
            background:#1fa971;
            color:white;
            padding:6px 12px;
            border-radius:20px;
        }
        a{
            text-decoration:none;
            margin-right:12px;
        }
    </style>
</head>
<body>

<div class="card">

<h1>🖥️ System Dashboard</h1>

<p>Deployment verification page.</p>

<table>
<tr><td>Hostname</td><td>{{hostname}}</td></tr>
<tr><td>Platform</td><td>{{platform}}</td></tr>
<tr><td>Python</td><td>{{python}}</td></tr>
<tr><td>Environment</td><td>{{env}}</td></tr>
<tr><td>Current Time</td><td>{{time}}</td></tr>
</table>

<br>

<span class="badge">Application Running</span>

<br><br>

<a href="/status">Status API</a>
<a href="/config">Configuration API</a>

</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML,
        hostname=socket.gethostname(),
        platform=platform.system(),
        python=platform.python_version(),
        env=os.getenv("ENVIRONMENT", "development"),
        time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

@app.route("/status")
def status():
    return jsonify({
        "status":"online",
        "hostname":socket.gethostname(),
        "timestamp":datetime.now().isoformat()
    })

@app.route("/config")
def config():
    return jsonify({
        "app_name":"System Dashboard",
        "version":os.getenv("APP_VERSION","1.0.0"),
        "environment":os.getenv("ENVIRONMENT","development"),
        "python_version":platform.python_version()
    })
@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT",5001))
    )

from flask import Flask, Response, request, send_from_directory, render_template_string
import os

app = Flask(__name__)

VIDEO_DIR = '/mnt/nvme/videos'

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Video streaming</title></head>
<body>
    <h1>Videos</h1>
    <ul>
    {% for video in videos %}
        <li><a href="/video/{{ video }}">{{ video }}</a></li>
    {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    videos = [f for f in os.listdir(VIDEO_DIR) if f.lower().endswith(('.mp4', '.mkv', '.avi'))]
    return render_template_string(HTML_TEMPLATE, videos=videos)

@app.route('/video/<path:filename>')
def video(filename):
    def generate():
        path = os.path.join(VIDEO_DIR, filename)
        with open(path, 'rb') as f:
            chunk = f.read(8192)
            while chunk:
                yield chunk
                chunk = f.read(8192)
    return Response(generate(), mimetype="video/mp4")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969, threaded=True) # nice

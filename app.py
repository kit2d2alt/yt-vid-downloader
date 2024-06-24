from flask import Flask, render_template, request, send_file, jsonify, send_from_directory
from pytube import YouTube
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/static/<path:filename>')
def staticfiles(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/get_info', methods=['POST'])
def get_info():
    url = request.form['url']
    yt = YouTube(url)
    video_info = {
        'title': yt.title,
        'thumbnail': yt.thumbnail_url,
        'streams': [
            {'resolution': stream.resolution, 'itag': stream.itag}
            for stream in yt.streams.filter(progressive=False, file_extension='mp4').order_by('resolution')
            if stream.resolution
        ]
    }
    return jsonify(video_info)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    itag = request.form['itag']
    yt = YouTube(url)
    stream = yt.streams.get_by_itag(itag)
    filename = f"{yt.title}.mp4"
    stream.download(filename=filename)
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

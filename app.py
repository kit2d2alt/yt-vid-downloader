from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    stream.download(filename='video.mp4')
    return send_file('video.mp4', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

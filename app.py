from flask import Flask, render_template, request, jsonify, send_file
import os
import uuid
import yt_dlp

app = Flask(__name__)

# Download folder banayein
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_tiktok_video(url):
    try:
        filename = f"{uuid.uuid4().hex}.mp4"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        
        ydl_opts = {
            'outtmpl': filepath,
            'format': 'best',
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'tiktok_video')
        
        return {
            'success': True,
            'filename': filename,
            'title': video_title,
            'size': os.path.getsize(filepath)
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url or 'tiktok.com' not in url:
        return jsonify({'success': False, 'error': 'Invalid TikTok URL'}), 400
    
    result = download_tiktok_video(url)
    return jsonify(result)

@app.route('/get-video/<filename>')
def get_video(filename):
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
from flask import Flask, request, render_template
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Google Drive API 설정
SERVICE_ACCOUNT_FILE = 'driveuploader-463205-7e7fccdb08c6.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_ID = '1xLL7Mqu767CMCk38gsOgwQiSOmAsKZ3r'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

def upload_to_drive(file_path, file_name):
    file_metadata = {
        'name': file_name,
        'parents': [FOLDER_ID]
    }
    media = MediaFileUpload(file_path, mimetype='image/png')
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    return file.get('id')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    name = request.form.get('name', 'unknown')
    file = request.files['file']
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    local_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(local_path)
    upload_to_drive(local_path, filename)
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

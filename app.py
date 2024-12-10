from flask import Flask, request, redirect, url_for, render_template, flash, session
import os
from werkzeug.utils import secure_filename
import uuid

# 初始化 Flask 應用
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 設置上傳目錄和允許的檔案類型
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 確保上傳目錄存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 檢查是否有檔案部分
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # 如果使用者沒有選擇檔案
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # 使用 uuid 生成唯一檔案名稱
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)

            # 生成完整圖片網址並保存到 session
            file_url = request.url_root.rstrip('/') + url_for('static', filename='uploads/' + unique_filename)
            session['file_url'] = file_url
            return redirect(url_for('upload_success'))
    return render_template('upload.html')

@app.route('/success', methods=['GET'])
def upload_success():
    file_url = session.get('file_url', None)
    if file_url is None:
        return redirect(url_for('upload_file'))
    return render_template('upload_success.html', file_url=file_url)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, send_file, url_for
import os
from encrypt import encrypt_image
from decrypt import decrypt_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ENCRYPTED_FOLDER'] = 'encrypted'
app.config['DECRYPTED_FOLDER'] = 'decrypted'
app.config['KEY_FOLDER'] = 'keys'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['ENCRYPTED_FOLDER'], exist_ok=True)
os.makedirs(app.config['DECRYPTED_FOLDER'], exist_ok=True)
os.makedirs(app.config['KEY_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    file = request.files['file']
    if file:
        input_image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_image_path)

        output_image_path = os.path.join(app.config['ENCRYPTED_FOLDER'], f"encrypted_{file.filename}")
        key_path = os.path.join(app.config['KEY_FOLDER'], f"{file.filename.split('.')[0]}_key.npy")

        encrypt_image(input_image_path, output_image_path, key_path)

        return render_template('result.html', action='encrypted', image_url=url_for('download_file', filename=output_image_path), key_url=url_for('download_file', filename=key_path))

@app.route('/decrypt', methods=['POST'])
def decrypt():
    file = request.files['file']
    key_file = request.files['key_file']
    if file and key_file:
        input_image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_image_path)

        key_path = os.path.join(app.config['KEY_FOLDER'], key_file.filename)
        key_file.save(key_path)

        output_image_path = os.path.join(app.config['DECRYPTED_FOLDER'], f"decrypted_{file.filename}")

        decrypt_image(input_image_path, key_path, output_image_path)

        return render_template('result.html', action='decrypted', image_url=url_for('download_file', filename=output_image_path))

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

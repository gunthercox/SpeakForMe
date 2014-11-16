import os
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from werkzeug import secure_filename
from time import gmtime, strftime


UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['wav'])

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    url_for('static', filename='css/main.css')
    url_for('static', filename='js/main.js')
    url_for('static', filename='js/recorder.js')
    url_for('static', filename='js/recorderWorker.js')
    url_for('static', filename='img/download.png')

    return render_template('index.html')

@app.route('/api/add', methods = ['POST'])
def post():
    from split.silence import convert_upload

    text = request.form['text']
    name = request.form['name']

    file = request.files['file']

    if file:
        path = "uploads/" + name

        if not os.path.exists(path):
            os.makedirs(path)
            os.makedirs("%s/words" % path)
            os.makedirs("%s/phonemes" % path)

    file_name = path + "/" + strftime("%Y-%m-%d_%H:%M:%S", gmtime())+".wav"

    file.save(file_name)

    convert_upload(file_name, text, name)

    return redirect('/')

@app.route('/play', methods = ['GET'])
def postSpeak():
    from flask import send_file
    from split.silence import get_phonemes
    import shutil
    import tempfile
    import wave

    text = request.args.get('text_input')
    name = request.args.get('name')

    words = text.split()

    temp = tempfile.NamedTemporaryFile(mode='w+b', suffix='wav')
    temp_wave = wave.open(temp, 'wb')

    temp_wave.setnchannels(2)
    temp_wave.setsampwidth(2)
    temp_wave.setframerate(44100)

    for word in words:
        phonemes = get_phonemes(str(word))

        for phoneme in phonemes:
            file_name = "uploads/%s/phonemes/%s/%s.wav" % (name, phoneme, word)

            if os.path.exists(file_name):
                phoneme_file = wave.open(file_name, 'rb')
                frames = phoneme_file.readframes(phoneme_file.getnframes())

                temp_wave.writeframes(frames)

        # throw some space in at the end of the word
        blank = '\x00\x00' * 5000

        temp_wave.writeframes(blank)

    temp_wave.close()

    temp.seek(0)

    return send_file(temp, mimetype="audio/wav", cache_timeout=0)

if __name__ == "__main__":
    app.config.update(
        DEBUG=True,
        SECRET_KEY="development"
    )
    app.run(host="0.0.0.0", port=8000)

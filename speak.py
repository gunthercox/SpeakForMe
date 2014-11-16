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
    text = request.form['text']
    name = request.form['name']
    print("text is '" + text + "'")
    print("name is '" + name + "'")
    file = request.files['file']
    
    if file:
	path = os.getcwd()+"/uploads/"+name
        if not os.path.exists(path):
    	    os.makedirs(path)
	file.save(path+"/"+strftime("%Y-%m-%d_%H:%M:%S", gmtime())+".wav")  

    

    return redirect('/')

if __name__ == "__main__":
    app.config.update(
        DEBUG=True,
        SECRET_KEY="development"
    )
    app.run(host="0.0.0.0", port=8000)

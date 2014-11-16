from flask import Flask
from flask import render_template
from flask import request, redirect, url_for

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    url_for('static', filename='css/main.css')
    url_for('static', filename='js/main.js')
    url_for('static', filename='js/recorder.js')
    url_for('static', filename='js/recorderWorker.js')
    return render_template('index.html')

@app.route('/data', methods = ['POST'])
def post():
    data = request.form['data']
    print("data is '" + data + "'")

   

    

    return redirect('/')

if __name__ == "__main__":
    app.config.update(
        DEBUG=True,
        SECRET_KEY="development"
    )
    app.run(host="0.0.0.0", port=8000)

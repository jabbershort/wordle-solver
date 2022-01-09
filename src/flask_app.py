#https://www.askpython.com/python-modules/flask/flask-forms

from flask import Flask,render_template,request

app = Flask(__name__,template_folder='templates')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/data/',methods = ['POST','GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit data"
    if request.method == 'POST':
        form_data = request.form
        return render_template('data.html',form_data = form_data)

app.run(host='0.0.0.0',port=5000)
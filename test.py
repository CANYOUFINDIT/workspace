from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('login.html')


@app.route('/a', methods=['GET', 'POST'])
def a():
    if request.method == 'GET':
        name = request.form.get('key')
        print name
        return 'hahaha'
    else:
        name = request.form.get('key')
        print name
        return 'e'

if __name__ == '__main__':
    app.run()
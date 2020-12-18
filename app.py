from flask import Flask, render_template, request, url_for, redirect


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('404error.html')


if __name__ == '__main__':
    app.run()

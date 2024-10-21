from flask import Flask, render_template, redirect, url_for, render_template, request
import pandas as pd
import main

app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

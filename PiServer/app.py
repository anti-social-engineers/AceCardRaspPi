from flask import Flask, request
from flask_restful import Resource, Api
import sys

sys.path.insert(0, '~/projects/AceCardRaspPi/func')

import test


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'

@app.route('/aceread')
def Read():
   return test

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
from __future__ import print_function
from flask import Flask
import sys
sys.path.append('../projects/PiServer/func')
from func import aceread
from func import text


app = Flask(__name__)
@app.route('/')
def index():
    return 'Hello world'

@app.route('/Read')
def Read():
   return text.test()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

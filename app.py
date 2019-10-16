from __future__ import division, print_function
import sys
import os
import glob
import re
import numpy as np

import time
from math import ceil
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')
'''
@app.route("/")
def hello():
    return "Hello World!"
'''
'''
if __name__ == '__main__':
    # Serve the app with gevent
    # http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server = WSGIServer(app)
    http_server.serve_forever()
'''
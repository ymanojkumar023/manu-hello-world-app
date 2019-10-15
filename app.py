from __future__ import division, print_function
import sys
import os
import glob
import re
import numpy as np

import time
from math import ceil

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
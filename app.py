from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

import time
from math import ceil

# Keras
from keras.models import load_model
from imageio import imread
from keras.preprocessing import image
from matplotlib import pyplot as plt

# Keras import from local function
from keras_loss_function.keras_ssd_loss import SSDLoss
from keras_layers.keras_layer_AnchorBoxes import AnchorBoxes
from keras_layers.keras_layer_L2Normalization import L2Normalization

from ssd_encoder_decoder.ssd_output_decoder import decode_detections, decode_detections_fast
from ssd_encoder_decoder.ssd_input_encoder import SSDInputEncoder

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

###################
###################
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# print('Setting parameters and loading our trained Model... ')
img_height = 300 # Height of the model input images
img_width = 300 # Width of the model input images
img_channels = 3 # Number of color channels of the model input images
mean_color = [123, 117, 104] # The per-channel mean of the images in the dataset. Do not change this value if you're using any of the pre-trained weights.
swap_channels = [2, 1, 0] # The color channel order in the original SSD is BGR, so we'll have the model reverse the color channel order of the input images.
n_classes = 1 # Number of positive classes, e.g. 20 for Pascal VOC, 80 for MS COCO
scales_pascal = [0.1, 0.2, 0.37, 0.54, 0.71, 0.88, 1.05] # The anchor box scaling factors used in the original SSD300 for the Pascal VOC datasets
scales_coco = [0.07, 0.15, 0.33, 0.51, 0.69, 0.87, 1.05] # The anchor box scaling factors used in the original SSD300 for the MS COCO datasets
scales = scales_pascal
aspect_ratios = [[1.0, 2.0, 0.5],
                 [1.0, 2.0, 0.5, 3.0, 1.0/3.0],
                 [1.0, 2.0, 0.5, 3.0, 1.0/3.0],
                 [1.0, 2.0, 0.5, 3.0, 1.0/3.0],
                 [1.0, 2.0, 0.5],
                 [1.0, 2.0, 0.5]] # The anchor box aspect ratios used in the original SSD300; the order matters
two_boxes_for_ar1 = True
steps = [8, 16, 32, 64, 100, 300] # The space between two adjacent anchor box center points for each predictor layer.
offsets = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5] # The offsets of the first anchor box center points from the top and left borders of the image as a fraction of the step size for each predictor layer.
clip_boxes = False # Whether or not to clip the anchor boxes to lie entirely within the image boundaries
variances = [0.1, 0.1, 0.2, 0.2] # The variances by which the encoded target coordinates are divided as in the original implementation
normalize_coords = True

__file__  = 'uploads'


def save_prediction(img_path, pred_decoded):
    orig_image = imread(img_path)
    
    colors = plt.cm.hsv(np.linspace(0, 1, n_classes+1)).tolist()
    classes = ['background','pool']
    plt.imshow(orig_image)
    current_axis = plt.gca()
    plt.axis('off')
    plt.savefig('static/preds/predicted_img.jpg', bbox_inches='tight', pad_inches = 0)
    plt.clf()
    plt.cla()
    plt.close()
    
    

#################
#################



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
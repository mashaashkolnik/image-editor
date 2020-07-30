"""
Primary Flask app

"""
import os
from flask import Flask, render_template, request
from flask_cors import CORS

from PIL import Image 

from .api import api as api_blueprint
from .errors import add_error_handlers
from .utils import serve_pil_image

from .imaging.filters import sobel_filter, canny_edge_detector, to_gray

def create_app():
    app = Flask(__name__, static_url_path='', 
        static_folder='web/static', template_folder='web/templates'
    )
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    add_error_handlers(app)
    return app

application = create_app()

@application.route("/")
@application.route("/index.html")
def index_page():
    return render_template('index.html')

@application.route("/stitch.html")
def stitch_page():
    return render_template('stitch.html')

@application.route("/upload", methods=["GET", "POST"])
def recieve_file():
    """ Recieve uploaded files from client.

    Returns:
        Response consisting of the processed image file and status code.
    """
    
    uploaded_files = request.files.getlist('file')  # get list of files uploaded

    file_ordering = request.values.get('order').split(',')
    file_ordering = [int(x) for x in file_ordering]

    files = [uploaded_files[i] for i in file_ordering]

    img_file = files[0]
    file_extention = img_file.filename.split('.')[-1]  # get file extension
    print('File received', img_file.filename)
    print('File extension', file_extention)
    
    with Image.open(img_file.stream) as img:
        # process PIL image (plugin processing functions here)
        img = to_gray(img)
        
        return serve_pil_image(img, file_extention), 200
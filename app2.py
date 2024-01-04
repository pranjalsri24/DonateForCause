from flask import Flask, flash,render_template,redirect,url_for,request
import cv2
import urllib.request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
directory = r'E:/Project/static/blurred'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello_world():
    return render_template('template.html')

@app.route("/", methods =['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #return render_template('index.html', filename=filename)
        return display_image(filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    filename1 = 'savedImage.jpg'
    image = cv2.imread('./static/uploads/'+filename)
    os.chdir(directory)
    Gaussian = cv2.GaussianBlur(image, (7, 7), 0)
    cv2.imwrite(filename1, Gaussian)
    #cv2.imshow('Gaussian Blurring', Gaussian)
    cv2.waitKey(0)
    print(filename1)
    return render_template('template.html', filename=filename1)   
 

if __name__ == "__main__" :
    app.run(debug=True)
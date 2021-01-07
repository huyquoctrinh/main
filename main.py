import pickle
import sklearn
from module.predict import test
import cv2
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template,request,redirect, url_for, send_from_directory
app =Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file',
                                filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	org =(50,50)
	font=cv2.FONT_HERSHEY_SIMPLEX
	color =(0, 0, 255)
	fontScale=2
	thickness=5
	PATH_TO_TEST_IMAGES_DIR = app.config['UPLOAD_FOLDER']
	TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR,filename.format(i)) for i in range(1, 2)]
	for image_path in TEST_IMAGE_PATHS:
		out = test(image_path)
    # return str(out)
		img=cv2.imread(image_path)
        # img=cv2.putText(img,out,(50, 50),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 255))
		img =cv2.resize(img,(500,500))
		img = cv2.putText(img, str(out), org, font, fontScale, 
                  color, thickness, cv2.LINE_AA, False)
		diachi ='uploads/'+filename
		cv2.imwrite(diachi, img)
	return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=5000)
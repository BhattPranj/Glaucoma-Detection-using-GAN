import os
import base64
import numpy as np
import io
from PIL import Image
from keras import backend as K
from skimage.measure import label,regionprops
import cv2
from skimage.transform import resize
from skimage.io import imsave
from keras.models import Model, load_model
from skimage.exposure import equalize_adapthist
import sqlite3
from flask import Flask, url_for, redirect, render_template, request, jsonify
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model


UPLOAD_FOLDER = 'static/Images'

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app = Flask(__name__)

def get_od_model():
    global modelod
    modelod = load_model('model/segment.hdf5',custom_objects={'dice_coef':dice_coef,'iu':iu,'iouLoss':iouLoss,'acc':acc,'IOU':IOU})
    print('*OD Model loaded!!')

def get_oc_model():
    global modeloc
    modeloc = load_model('model/model.hdf5',custom_objects={'dice_coef':dice_coef,'iu':iu,'iouLoss':iouLoss,'acc':acc,'IOU':IOU})
    print('*OC Model loaded!!')


def preprocessOD():
    global image
    image=equalize_adapthist(np.array(Image.open('./static/Images/input.jpg').resize([128,128],Image.BICUBIC)))
    image=image.reshape([1,128,128,3])
    image/=np.max(image)
    image-=np.mean(image)
    image/=np.std(image)
    return image
def preprocessOC(image1):
    global mir,mic,mar,mac
    im=image1
    li=label(im+0.5)
    region=regionprops(li)
    mir,mic,mar,mac=region[0].bbox
    cx=image[0,mir:mar,mic:mac,:]
    c_x=cv2.resize(cx,(128,128),interpolation=cv2.INTER_AREA)
    c_x=c_x.reshape([1,128,128,3])
    return c_x
def dice_coef(y_true, y_pred):
    intersection = K.sum(y_true * y_pred)
    return (2. * intersection + 1) / (K.sum(y_true) + K.sum(y_pred) + 1)
#%%
def iu(y_true, y_pred):
    a2=K.sum(y_true*y_true)
    b2=K.sum(y_pred*y_pred)
    iu=K.sum(y_true*y_pred)/(a2+b2-K.sum(y_true*y_pred))
    return iu
#%%
def iouLoss(y_true, y_pred):
    return-K.log(iu(y_true,y_pred))
#%%
def acc(y_true, y_pred):
    TP = K.sum(y_true * y_pred)
    FP=K.sum((K.max(y_true)-y_true) * y_pred)
    return (TP)/(TP+FP)

#%%
def IOU(y_true, y_pred):
    intersection = K.sum(y_true * y_pred)
    union=K.sum((y_true+y_pred)/2)
    iou=intersection/union
    return iou

print("* Loading OD segmentation Model")
get_od_model()
print("* Loading OC segmentation Model")
get_oc_model()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/sign")
def sign():
    return render_template("signup-in.html")

@app.route("/signup")
def signup():
    
    
    name = request.args.get('user','')
    password = request.args.get('pass','')
    password1 = request.args.get('pass1','')
    email = request.args.get('email','')
    number = request.args.get('num','')

    if password1 == password:
        con = sqlite3.connect('signup.db')
        cur = con.cursor()
        cur.execute("insert into `datas` (`name`, `password`,`password1`,`email`,`mobile`) VALUES (?, ?, ?, ?, ?)",(name,password,password1,email,number))
        con.commit()
        con.close()

        return render_template("signup-in.html")
    
    else:
        
        return render_template("signup-in.html")


@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('pass','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `name`, `password` from datas where `name` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signup-in.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("tool.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("tool.html")
    else:
        return render_template("signup-in.html")

@app.route("/tool")
def tool():
	return render_template("tool.html")

@app.after_request
def add_header(response):
   
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route("/upload",methods=['POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		filename = secure_filename(file.filename)
		os.remove('./static/Images/input.jpg')
		file.save('static/Images/input.jpg')
	    #return redirect(url_for('uploaded_file',filename=filename))
	    #return render_template("tool.html")
	return redirect(url_for('tool'))

@app.route("/preidct")
def predict():
    im1=preprocessOD()
    y_od=modelod.predict(im1, verbose=1)
    y_od=y_od.reshape([128,128])
    os.remove('static/Images/od.jpg')
    imsave('static/Images/od.jpg', y_od)
    im2=preprocessOC(y_od)
    y_oc=modeloc.predict(im2, verbose=1)
    y_oc=y_oc.reshape([128,128])
    oc_pred=np.zeros([128,128],dtype='float32')
    cx=cv2.resize(y_oc,((mac-mic),(mar-mir)),interpolation=cv2.INTER_AREA)
    oc_pred[mir:mar,mic:mac]=cx
    os.remove('static/Images/oc.jpg')
    imsave('static/Images/oc.jpg', oc_pred)
    li1=label(y_od+0.5)
    li2=label(oc_pred+0.5)
    region1=regionprops(li1)
    region2=regionprops(li2)
    mir1,mic1,mar1,mac1=region1[0].bbox
    mir2,mic2,mar2,mac2=region2[0].bbox
    OD_Diam=mac1-mic1
    OC_Diam=mac2-mic2
    CDR=OC_Diam/OD_Diam
    print(CDR)
    g_h= 1 if CDR>0.5 else 0
    if (g_h):
        response=  '***THE PREDICTED RESULT FOR THE GIVEN PATIENT IMAGE IS : GLAUCOMATIC!!! ***'
        
        print(' *** GLAUCOMATIC!!! ***')

        return render_template('tool.html',preds = response)
    else:
        response= '***THE PREDICTED RESULT FOR THE GIVEN PATIENT IMAGE IS : HEALTHY!!! ***' 
        print(' *** HEALTHY!!! ***')

        return render_template('tool.html',preds = response)


model =load_model("model/model.h5")
 
print('@@ Model loaded')
 
 
def pred_cot_dieas(cott_plant):
  test_image = load_img(cott_plant, target_size = (224, 224)) # load image 
  print("@@ Got Image for prediction")
   
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
   
  result = model.predict(test_image).round(3) # predict diseased palnt or not
  print('@@ Raw result = ', result)
   
  pred = np.argmax(result) # get the index of max value
 
  if pred == 0:
    return "GLAUCOMA", 'index.html' 
  elif pred == 1:
      return 'NOT GLAUCOMA', 'index.html' 
  else:
    return "Invaild Image", 'index.html' # if index 3


@app.route("/index", methods=['GET', 'POST'])
def index():
        return render_template('index.html')
     

  
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict1", methods = ['GET','POST'])
def predict1():
     if request.method == 'POST':
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
         
        file_path = os.path.join('static/uploads', filename)
        file.save(file_path)
 
        print("@@ Predicting class......")
        pred, output_page = pred_cot_dieas(cott_plant=file_path)
               
        return render_template(output_page, pred_output = pred, user_image = file_path)

if __name__ == "__main__":
    app.run(debug=True)
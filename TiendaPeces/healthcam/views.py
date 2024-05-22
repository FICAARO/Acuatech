from django.http import HttpResponse
from django.shortcuts import render, redirect
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings 
from tensorflow.python.keras.backend import set_session
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from rembg import remove 
from PIL import Image 
import os
def remove_background(input_path,output_path):
    print(os.getcwd())
    input_img = Image.open(input_path) 
    output_img = remove(input_img).convert('RGB')
    output_img.save(output_path) 

def predict_image_class(image_path):
    target_size_square=256
    model = load_model('../models/fishes_46.h5')
    test=["atacado_tumor_y_deformidad",  "girodactilo","hidropecia_y_vegiga_nadatoria","huecos en la cabesa",   "nopez","parasito_en_la_boca", "quemadura_bagre", "branquias","gusano_lernea"   ,"hongos","ich_punto_planco","ojo_picho","podredumbre aleta","sanos"]
    img = image.load_img(image_path, target_size=(target_size_square, target_size_square))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.

    prediction = model.predict(img_array)[0]
    max_val=0
    max_pos=0
    print(prediction)
    for i in range(len(prediction)):
        print("  col ",i,prediction,prediction[i])
        if max_val<prediction[i]:
            max_val=prediction[i]
            max_pos=i
    print(prediction,len(prediction),"max value",max_val)
    return test[max_pos] ,max_val



def healthcamIndex(request):
    if  request.method == "POST":
        enable=True
        f=request.FILES['sentFile'] # here you get the files needed
        response = {}
        file_name = "fishdiases/pic.jpg"
        file_name_rbg = "fishdiases/pic_rbg.jpg"

        file_name_2 = "media/"+default_storage.save(file_name, f)
        print(file_name_2)
        remove_background(file_name_2,"media/"+file_name_rbg)
        file_url = default_storage.url(file_name_rbg)

        print(file_url[1:])
        #original = load_img(file_url[1:], target_size=(224, 224))
        #numpy_image = img_to_array(original)
        
        label,percent=predict_image_class(file_url[1:])

        response['name'] = str(label)
        response['percent'] = str(percent)
        response['enable'] = enable

        return render(request,'healthcam2.html',response)
    else:

        return render(request,'healthcam2.html')
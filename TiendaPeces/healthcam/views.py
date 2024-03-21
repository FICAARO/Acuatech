from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import healthcam
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf
import os
from django.shortcuts import render
from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings 
from tensorflow.python.keras.backend import set_session
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import decode_predictions
import matplotlib.pyplot as plt
import numpy as np
import datetime
import traceback


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
    return test[max_pos]



def healthcamIndex2(request):
    if  request.method == "POST":
        f=request.FILES['sentFile'] # here you get the files needed
        response = {}
        file_name = "fishdiases/pic.jpg"
        file_name_2 = default_storage.save(file_name, f)
        file_url = default_storage.url(file_name_2)
        print(file_url[1:])
        #original = load_img(file_url[1:], target_size=(224, 224))
        #numpy_image = img_to_array(original)
        
        label=predict_image_class(file_url[1:])

        response['name'] = str(label)
        return render(request,'healthcam2.html',response)
    else:
        return render(request,'healthcam2.html')
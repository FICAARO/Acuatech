from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.clickjacking import xframe_options_exempt

import os
import pandas as pd


def writetxt(name,content,mode="w"):
  """
  writetxt(name,content) , write in txt file something  
  """
  content=str(content)
  with open(name, mode) as file:
    file.write(content)
    file.close()
def genMap(data,name):
  import folium
  m = folium.Map(location=[6.256405968932449, -75.59835591123756])
  #folium.TileLayer('Mapbox Control Room').add_to(m)
  for i in range(len(data)):
    popup=data["name"][i]+"<li>"+data["dashboard"][i]+"</li><br>"
    folium.Marker([float(data["lat"][i]),float(data["lng"][i])], popup=popup, tooltip=data["name"][i]).add_to(m)
  m.save(name)
def nullValue(val,newval="-"):
    if not val or val=="":
        return newval 

DATAPATH = "map_fishtanks/data.csv"
MAPNAME = "map_fishtanks/templates/map.html"

# Create a Django view
def index_map(request):
    return render(request, "map_viewer.html")
@xframe_options_exempt
def mapweb(request):
    return render(request, "map.html")

@csrf_protect
def addData(request):
    if request.method == "POST":
        name = request.POST.get("name")
        dashboard = request.POST.get("dashboard")
        lat = request.POST.get("lat")
        lng = request.POST.get("lng")
        data = f"{name},{dashboard},{lat},{lng}\n"
        writetxt(DATAPATH, data, "a")
        df = pd.read_csv(DATAPATH)
        genMap(df, f"{MAPNAME}")
    return render(request, "addData.html")
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User  
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from .models import Dashboards

from dotenv import load_dotenv
from os import environ, path
import json
import jwt

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS

load_dotenv(path.join(path.dirname(path.abspath(__file__)), "..", "influx.env"))
load_dotenv(path.join(path.dirname(path.abspath(__file__)), "..", "dashboard.env"))

ORG = environ.get("ORG")
BUCKET = environ.get("BUCKET")
URL = environ.get("URL")
TOKEN = environ.get("TOKEN")

ENCODING_KEY = environ.get("ENCODING_KEY")

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=ASYNCHRONOUS)
query_api = client.query_api()

# Create your views here.
def dashboard(request):
    session_id = request.COOKIES.get("sessionid")
    session = Session.objects.get(session_key=session_id)
    session_data = session.get_decoded()

    user_id = session_data.get('_auth_user_id')
    user = User.objects.get(id=user_id)

    dashboards = None
    dashboards = user.dashboards.all()
    if request.method == "GET":
        if dashboards.count() == 0:
            return render(request, "generate.html", { "token": None })

        print(dashboards.count())
        print(user.username, user.password, ENCODING_KEY)
        
        return render(request, "dashboard.html", { "name": user.dashboards.first().name })
    elif request.method == "DELETE":
        dashboards.delete()
        return JsonResponse({ "msg": "Deleted this user dashboard successfully." }, status=202)

def generate(request):
    if (request.method != "GET"): return JsonResponse({ "code": 400 })
    
    session_id = request.COOKIES.get("sessionid")
    session = Session.objects.get(session_key=session_id)
    session_data = session.get_decoded()

    user_id = session_data.get('_auth_user_id')
    user = User.objects.get(id=user_id)

    dashboard_name = request.GET.get("dashboard-name")
    existing = Dashboards.objects.filter(name=dashboard_name, user=user)
    if existing: redirect("dashboard")

    print("creating")

    dashboard = Dashboards(
        user=user,
        name=dashboard_name,
        extra1_label='Plug 1',
        extra2_label='Plug 2',
        extra3_label='Plug 3',
    )

    dashboard.save()
    token = jwt.encode({ "username": user.username, "password": user.password, "dashboard": dashboard_name  }, key=ENCODING_KEY, algorithm="HS256")
    user.dashboards

    return render(request, "generate.html", { "token": token })

@csrf_exempt
def data(request):
    user = None
    dashboards = None
    source = request.headers["X-Request-Source"] 
    match source:
        case "Website":
            session_id = request.COOKIES.get("sessionid")
            session = Session.objects.get(session_key=session_id)
            session_data = session.get_decoded()

            user_id = session_data.get('_auth_user_id')
            user = User.objects.get(id=user_id)

            dashboards: Dashboards = user.dashboards.first()
        case "ESP32":
            token = request.headers["X-User-Token"]
            payload = None
            try:
                payload = jwt.decode(token, ENCODING_KEY, algorithms=["HS256"])
            except jwt.exceptions.DecodeError:
                print("[ESP32] Invalid token")
                return JsonResponse({ "code": 400, "msg": "Invalid token" })

            user = User.objects.filter(username=payload["username"], password=payload["password"]).first()
            dashboards = user.dashboards.first()
        case _:
            pass

    print(request.method, user, dashboards, source)

    match request.method:
        case "GET":
            query = f"""from(bucket: "influxdb")
                |> range(start: -15s)
                |> filter(fn: (r) => r["_measurement"] == "aquarium")
                |> filter(fn: (r) => r["user"] == "{user.username}")
                |> filter(fn: (r) => r["name"] == "{dashboards.name}")
                |> last()"""
            res = query_api.query(org=ORG, query=query)
            r = {
                "temp": None,
                "hum": None,
                "wtemp": None,
                "wlevel": None,
                "turbp": None,
                "lights": None,
                "filter": None,
                "thermo": None,
                "plug1Label": None,
                "plug2Label": None,
                "plug3Label": None
            }
            for table in res:
                for rec in table.records:
                    if rec.get_field() not in r: continue
                    r[rec.get_field()] = rec.get_value()

            r["lights"] = int(dashboards.extra1_state)
            r["filter"] = int(dashboards.extra2_state)
            r["thermo"] = int(dashboards.extra3_state)
            r["plug1Label"] = dashboards.extra1_label
            r["plug2Label"] = dashboards.extra2_label
            r["plug3Label"] = dashboards.extra3_label
            print(r)

            return JsonResponse(r)
        case "POST":
            json_data = json.loads(request.body)
            
            if source == "Website":
                dashboards.extra1_state = json_data["lights"] == 1
                dashboards.extra2_state = json_data["filter"] == 1
                dashboards.extra3_state = json_data["thermo"] == 1
                dashboards.save()
            elif source == "ESP32":
                record = Point("aquarium").tag("user", user.username).tag("name", dashboards.name)
                record.field("temp", float(round(json_data["temp"], 1)))
                record.field("hum", float(round(json_data["hum"], 1)))
                record.field("wtemp", float(round(json_data["wtemp"], 1)))
                record.field("wlevel", float(round(json_data["wlevel"], 1)))
                record.field("turbp", float(round(json_data["turbp"], 1)))
                print(record.to_line_protocol())
                res = write_api.write(bucket=BUCKET, org=ORG, record=record)

            return JsonResponse({ "code": 200 })
        case "PUT":
            print(request.body)
            json_data = json.loads(request.body)

            if source == "Website":
                dashboards.extra1_label = json_data["plug1Label"]
                dashboards.extra2_label = json_data["plug2Label"]
                dashboards.extra3_label = json_data["plug3Label"]
                dashboards.save()
            
            return JsonResponse({ "code": 202 })

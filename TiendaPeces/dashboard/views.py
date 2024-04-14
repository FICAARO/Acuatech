from django.shortcuts import render
from django.http import JsonResponse

from dotenv import load_dotenv
import json
from os import environ, path

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS

load_dotenv(path.join(path.dirname(path.abspath(__file__)), "..", "influx.env"))

ORG = environ.get("ORG")
BUCKET = environ.get("BUCKET")
URL = environ.get("URL")
TOKEN = environ.get("TOKEN")

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=ASYNCHRONOUS)
query_api = client.query_api()


# Create your views here.
def dashboard(request):
    return render(request, "dashboard.html")

def data(request):
    match request.method:
        case "GET":
            query = 'from(bucket: "influxdb")'\
                '|> range(start: -30m)'\
                '|> filter(fn: (r) => r["_measurement"] == "test")'\
                '|> filter(fn: (r) => r["device"] == "esp32_ns")'\
                '|> last()'
            res = query_api.query(org=ORG, query=query)
            r = {}
            for table in res:
                for rec in table.records:
                    r[rec.get_field()] = rec.get_value()

            return JsonResponse(r)
        case "POST":
            json_data = json.loads(request.body)
            lights = json_data.get('lights', None)
            filter = json_data.get('filter', None)
            thermo = json_data.get('thermo', None)

            record = Point("test").tag("device", "esp32_ns").field("lights", lights).field("filter", filter).field("thermo", thermo)
            write_api.write(bucket=BUCKET, org=ORG, record=record)
            
            return JsonResponse({ "code": 200 })

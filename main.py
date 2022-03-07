import base64
import json
import os.path

import requests
from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
from datetime import datetime
from datetime import timedelta

import services.service as service

app = Flask(__name__)
CORS(app)

# image_path = "/Users/Pontagun/Public/Project/APReporter/src/assets/image/"
aqiCNToken = "6f0bd0ed71ccee8988757f353b8a920deaa0741a"
weatherToken = "220aabafd04062943967fc23974cc8d5"


@app.route('/air4thai')
def air4thai_value():
    arg = request.args
    rec = {"suite": []}
    station = "https://airkm-a4th.datascience.cmu.ac.th/api/latest?lat=" + \
        arg['lat'] + "&long=" + arg['lon']

    contents = requests.get(station)
    aq_data = json.loads(contents.content.decode('utf-8'))
    recommend_data = service.get_recommendation()
    rec["suite"] = recommend_data

    service.log('air4thai', str(aq_data), "lat=" +
                arg['lat'] + "&lon=" + arg['lon'])

    if contents.status_code == 200:
        return jsonify({**aq_data, **rec})
    else:
        return None


@app.route('/dustboy')
def dustboy_value():
    arg = request.args
    rec = {"suite": []}
    station = "https://www.cmuccdc.org/api/ccdc/value/" + arg['station']

    contents = requests.get(station)
    aq_data = json.loads(contents.content.decode('utf-8'))
    recommend_data = service.get_recommendation()
    rec["suite"] = recommend_data

    service.log('dustboy', str(aq_data), arg['station'])

    if contents.status_code == 200:
        return jsonify({**aq_data, **rec})
    else:
        return None


@app.route('/iqair')
def iqair_value():
    arg = request.args
    rec = {"suite": []}
    lat = arg['lat']
    lon = arg['lon']
    url = "https://airkm-backend.docker.titipat.net/api/iqair"

    contents = requests.get(url, params={
        'lat': lat,
        'lon': lon
    })
    aq_data = json.loads(contents.content.decode('utf-8'))
    recommend_data = service.get_recommendation()
    rec["suite"] = recommend_data

    service.log('iqair', str(aq_data), "lat=" +
                arg['lat'] + "&lon=" + arg['lon'])

    if contents.status_code == 200:
        return jsonify({**aq_data, **rec})
    else:
        return None


@app.route('/aqicn')
def aqicn_value():
    arg = request.args
    rec = {"suite": []}
    station = "https://api.waqi.info/feed/geo:" + \
        arg['lat'] + ";" + arg['lon'] + "/?token=" + aqiCNToken

    contents = requests.get(station)
    aq_data = json.loads(contents.content.decode('utf-8'))
    recommend_data = service.get_recommendation()
    rec["suite"] = recommend_data

    service.log('aqicn', str(aq_data), "lat=" +
                arg['lat'] + "&lon=" + arg['lon'])

    daily_forecast_pm25 = aq_data["data"]["forecast"]["daily"]["pm25"]
    daily_forecast_len = len(daily_forecast_pm25)
    if daily_forecast_len < 9:
        for i in range(8 - daily_forecast_len):
            day = str(datetime.strptime(daily_forecast_pm25[daily_forecast_len - 1]["day"], "%Y-%m-%d") + timedelta(
                days=i + 1))
            m = {"avg": "-", "day": day.split(" ")[0], "min": "-", "max": "-"}
            aq_data["data"]["forecast"]["daily"]["pm25"].append(m)

    if contents.status_code == 200:
        return jsonify({**aq_data, **rec})
    else:
        return None


@app.route('/weather')
def weather_value():
    arg = request.args

    station = "https://api.openweathermap.org/data/2.5/onecall?lat=" \
              + str(arg['lat']) + "&lon=" + str(arg['lon']) \
              + "&exclude=minutely,hourly&appid=" + weatherToken
    contents = requests.get(station)

    if contents.status_code == 200:
        return jsonify(json.loads(contents.content.decode('utf-8')))
    else:
        return None


@app.route('/news')
def news():
    json_data = service.get_wiki(1)
    for obj in json_data:
        obj["data"] = base64.b64encode(obj["data"]).decode("utf-8")

    return jsonify(json_data)


@app.route('/wiki')
def wiki():
    json_data = service.get_wiki(2)

    return jsonify(json_data)


@app.route('/recommendation', methods=['PUT'])
def set_recommendation():
    content = request.json
    result = service.set_recommendation(content["red"], content["orange"], content["yellow"], content["green"],
                                        content["blue"])
    return result


@app.route('/recommendation')
def get_recommendation():
    json_data = service.get_recommendation()

    return jsonify(json_data)


@app.route('/specialist')
def specialist():
    specialists = []
    json_data = service.get_specialist()
    data = str(json_data[0]["content"]).splitlines()

    for idx in range(0, len(data), 6):
        person = {"name": data[idx].replace("## ", ""), "memberof": data[idx + 1].replace("###### ", ""),
                  "position": data[idx + 2].replace("###### ", ""), "email": data[idx + 3].replace("###### ", ""),
                  "tel": data[idx + 4].replace("###### ", ""), "id": data[idx + 5].replace("###### ", "")}
        specialists.append(person)

    return jsonify(specialists)


if __name__ == '__main__':
    app.run()

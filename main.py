import json
import os.path
from os import path

import mysql.connector
import requests
from flask import Flask, request
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

image_path = "/Users/Pontagun/Public/Project/APReporter/src/assets/image/"

@app.route('/dustboy')
def dustboyValue():
    # username = request.args.get('username')
    arg = request.args

    station = "https://www.cmuccdc.org/api/ccdc/value/" + arg['station']

    contents = requests.get(station)

    if contents.status_code == 200:
        return jsonify(json.loads(contents.content.decode('utf-8')))
    else:
        return None

@app.route('/news')
def news():
    cnx = mysql.connector.connect(user='root', password='Pontakorn2', database='wiki', use_unicode=True, charset='utf8')
    cursor = cnx.cursor()

    query = (
        "select x.id, x.path, x.title, x.description, x.image, y.data "
        "from "
        "(	select ps.id, ps.path, ps.title, ps.description, pt.tagId ,substr(ps.content, 34, locate('\"></figure>', ps.content) - 34) image "
        "	from pages ps inner join pageTags pt on ps.id = pt.pageId where pt.tagId = 1"
        ") x left join "
        "("
        "	select a.id, a.filename, b.data from assets a left join assetData b on a.id = b.id"
        ") y on x.image = y.filename order by x.id desc;")

    cursor.execute(query)

    row_headers = [x[0] for x in cursor.description]  # this will extract row headers
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    cursor.close()
    cnx.close()

    for obj in json_data:
        image = obj["data"]
        write_file(image, os.path.join(image_path, obj["image"]))
        del obj["data"]

    return jsonify(json_data)


@app.route('/wiki')
def wiki():
    cnx = mysql.connector.connect(user='root', password='Pontakorn2', database='wiki', use_unicode=True, charset='utf8')
    cursor = cnx.cursor()

    query = (
        "select x.id, x.path, x.title, x.description, x.image, y.data "
        "from "
        "(	select ps.id, ps.path, ps.title, ps.description, pt.tagId ,substr(ps.content, 34, locate('\"></figure>', ps.content) - 34) image "
        "	from pages ps inner join pageTags pt on ps.id = pt.pageId where pt.tagId = 2"
        ") x left join "
        "("
        "	select a.id, a.filename, b.data from assets a left join assetData b on a.id = b.id"
        ") y on x.image = y.filename order by x.id desc;")

    cursor.execute(query)

    row_headers = [x[0] for x in cursor.description]  # this will extract row headers
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    cursor.close()
    cnx.close()

    for obj in json_data:
        image = obj["data"]
        write_file(image, os.path.join(image_path, obj["image"]))
        del obj["data"]

    return jsonify(json_data)


def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    if (not path.exists(filename)):
        with open(filename, 'wb') as file:
            file.write(data)


if __name__ == '__main__':
    app.run()

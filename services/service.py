from os import path
from flask import jsonify
import mysql.connector


# cnx = mysql.connector.connect(user='wikijs',
#                               password='wikijsrocks',
#                               database='wiki',
#                               use_unicode=True,
#                               charset='utf8',
#                               port=3306, host="db")

def log(s, d, param):
    cnx = mysql.connector.connect(user='wikijs',
                                  password='wikijsrocks',
                                  database='wiki',
                                  use_unicode=True,
                                  charset='utf8',
                                  port=3306, host="db")
    # cnx = mysql.connector.connect(user='root', password='Pontakorn2', database='wiki', use_unicode=True,
    #                               charset='utf8',
    #                               port=3306, host="localhost")
    cursor = cnx.cursor()
    query = ("create table IF NOT EXISTS airkmLog ("
             "Id int auto_increment not null primary key,"
             "Source varchar(255) not null,"
             "Data TEXT not null,"
             "Parameter TEXT not null,"
             "Date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
             ");")

    cursor.execute(query)
    insert_sql = "insert into airkmLog(Source, Data, Parameter) values (\"{}\", \"{}\", \"{}\");".format(
        s.replace("\"", "'"), d.replace("\"", "'"), param.replace("\"", "'"))

    cursor.execute(insert_sql)
    cursor.close()

    cnx.commit()
    cnx.close()


def get_wiki(tag_id):
    cnx = mysql.connector.connect(user='wikijs',
                                  password='wikijsrocks',
                                  database='wiki',
                                  use_unicode=True,
                                  charset='utf8',
                                  port=3306, host="db")
    # cnx = mysql.connector.connect(user='root', password='Pontakorn2', database='wiki', use_unicode=True,
    #                               charset='utf8',
    #                               port=3306, host="localhost")
    cursor = cnx.cursor()
    if (tag_id == 1):
        query = (
            "select x.id, x.path, x.title, x.description, x.image, y.data "
            "from "
            "(	select ps.id, ps.path, ps.title, ps.description, pt.tagId ,substr(ps.content, 34, locate('\"></figure>', "
            "ps.content) - 34) image "
            "	from pages ps inner join pageTags pt on ps.id = pt.pageId where pt.tagId = {}"
            ") x left join "
            "("
            "	select a.id, a.filename, b.data from assets a left join assetData b on a.id = b.id"
            ") y on x.image = y.filename where y.data is not Null order by x.id desc;").format(tag_id)
    elif (tag_id == 2):
        query = (
            "select ps.id, ps.path, ps.title, pt.tagId "
            "from pages ps inner join pageTags pt on ps.id = pt.pageId "
            "where pt.tagId = {} order by ps.title asc").format(tag_id)

    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]  # this will extract row headers
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    cursor.close()
    cnx.close()
    return json_data


def get_recommendation():
    cnx = mysql.connector.connect(user='wikijs',
                                  password='wikijsrocks',
                                  database='wiki',
                                  use_unicode=True,
                                  charset='utf8',
                                  port=3306, host="db")
    # cnx = mysql.connector.connect(user='root', password='Pontakorn2', database='wiki', use_unicode=True,
    #                               charset='utf8',
    #                               port=3306, host="localhost")
    cursor = cnx.cursor()
    query = "select Id, Color, Detail from airkmInput order by id;"
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]  # this will extract row headers
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    cursor.close()
    cnx.close()
    return json_data


def set_recommendation(red, orange, yellow, green):
    cnx = mysql.connector.connect(user='wikijs',
                                  password='wikijsrocks',
                                  database='wiki',
                                  use_unicode=True,
                                  charset='utf8',
                                  port=3306, host="db")
    # cnx = mysql.connector.connect(user='root', password='Pontakorn2', database='wiki', use_unicode=True,
    #                               charset='utf8',
    #                               port=3306, host="localhost")
    cursor = cnx.cursor()
    query = "update airkmInput set Detail='{}' where id = 1".format(red)
    print(query)
    cursor.execute(query)
    cnx.commit()
    query = "update airkmInput set Detail='{}' where id = 2".format(orange)
    cursor.execute(query)
    cnx.commit()
    query = "update airkmInput set Detail='{}' where id = 3".format(yellow)
    cursor.execute(query)
    cnx.commit()
    query = "update airkmInput set Detail='{}' where id = 4".format(green)
    cursor.execute(query)
    cnx.commit()

    cursor.close()
    cnx.close()
    return jsonify({'result': 200})


def get_specialist():
    cnx = mysql.connector.connect(user='wikijs',
                                  password='wikijsrocks',
                                  database='wiki',
                                  use_unicode=True,
                                  charset='utf8',
                                  port=3306, host="db")
    # cnx = mysql.connector.connect(user='root', password='Pontakorn2', database='wiki', use_unicode=True,
    #                               charset='utf8',
    #                               port=3306, host="localhost")
    cursor = cnx.cursor()
    query = "select content from pages where title = \"Specialist\";"
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    cursor.close()
    cnx.close()
    return json_data


def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    if not path.exists(filename):
        with open(filename, 'wb') as file:
            file.write(data)

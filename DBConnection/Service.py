from sys import path

import mysql.connector


def getWiki(tagId):
    cnx = mysql.connector.connect(user='root', password='Pontakorn2', database='wiki', use_unicode=True, charset='utf8')
    cursor = cnx.cursor()

    query = (
        "select x.id, x.path, x.title, x.description, x.image, y.data "
        "from "
        "(	select ps.id, ps.path, ps.title, ps.description, pt.tagId ,substr(ps.content, 34, locate('\"></figure>', ps.content) - 34) image "
        "	from pages ps inner join pageTags pt on ps.id = pt.pageId where pt.tagId = {}"
        ") x left join "
        "("
        "	select a.id, a.filename, b.data from assets a left join assetData b on a.id = b.id"
        ") y on x.image = y.filename order by x.id desc;").format(tagId)

    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]  # this will extract row headers
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

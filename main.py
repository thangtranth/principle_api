import flask
from flask import request, jsonify
# import mysql.connector
# from mysql.connector import Error
import key_word_search

app = flask.Flask(__name__)
# app.config['Debug'] = True
# try:
#     connection = mysql.connector.connect(host='localhost',
#                                          database='principles',
#                                          user='root')
#     if connection.is_connected():
#         db_Info = connection.get_server_info()
#         print("Connected to MySQL Server version ", db_Info)
#         cursor = connection.cursor()
#         cursor.execute("select database();")
#         record = cursor.fetchone()
#         print("You're connected to database: ", record)
#
# except Error as e:
#     print("Error while connecting to MySQL", e)
#

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


# # API:
# @app.route('/api/v1/principle', methods=['GET'])
# def get_principle():
#     query_parameters = request.args
#     situation = query_parameters.get('situation')
#     print(situation)
#     query = "SELECT principle FROM situation_principle WHERE situation=%s;"
#     cursor.execute(query, (situation,))
#     principles = cursor.fetchall()
#     print(principles)
#     row_header = [x[0] for x in cursor.description]
#     print(row_header)
#     json_data = []
#     for result in principles:
#         json_data.append(dict(zip(row_header, result)))
#     return jsonify(json_data)


@app.route('/api/v1/principle_para', methods=['GET'])
def get_para():
    query_parameters = request.args
    key_word = query_parameters.get('key_word') 
    search = key_word_search.KeyWordSearch()
    return jsonify(search.query(key_word))


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run()

import flask
import json
import os
from werkzeug import exceptions
from datetime import datetime
    
app = flask.Flask(__name__)

working_directory = "/opt/garbage-collector-api" 

def load_json():
    """
    load json file gvu_stpoelten.json to api
    """

    try:
        with open(working_directory + "/gvu_stpoelten.json",'r') as jf:
            neu_datetime = list()
            for item in json.load(jf):
                neu_datetime.append({'date':(datetime.strptime(item['date'],'%Y-%m-%d %H:%M')).replace(tzinfo=None),'garbage_container_type':item['garbage_container_type']})
            return neu_datetime
        
    except FileNotFoundError as e:
        return  exceptions.InternalServerError(description="File Not found. Directory: {0}".format(working_directory))
        
    except Exception as e:
        return exceptions.InternalServerError(description=e)


@app.route("/all/",methods=["GET"])
def garbage_collector():
    return flask.jsonify(load_json())

@app.route("/next/",methods=["GET"])
def get_next():
    garbage_list = load_json()

    """
    get now
    """
    now = datetime.now()

    """
    get next item and return it
    """
    for item in garbage_list:
        if item['date'] < now:
            continue
        if item['date'] >= now:
            return flask.jsonify(item)


if __name__ == '__main__':
    app.run()

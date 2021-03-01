import flask
import json
import os
from werkzeug import exceptions

app = flask.Flask(__name__)
app.config["DEBUG"] = True

working_directory = os.getcwd()

@app.route("/garbage_collector",methods=["GET"])
def garbage_collector():
    """
    load json file gvu_stpoelten.json to api
    """

    try:
        with open(working_directory + "/gvu_stpoelten.json",'r') as jf:
            return flask.jsonify(json.load(jf))
    
    except FileNotFoundError as e:
        return  exceptions.InternalServerError(description=e)
    
    except Exception as e:
        return exceptions.InternalServerError(description=e)


app.run()
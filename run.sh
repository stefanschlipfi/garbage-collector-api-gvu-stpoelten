source /opt/garbage-collector-api/venv/bin/activate
export FLASK_APP=/opt/garbage-collector-api/flask_app.py

export PATH=$PATH:/opt/garbage-collector-api/
flask run --host 127.0.0.1 --port=8080
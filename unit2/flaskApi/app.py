from flask import  jsonify,Flask
from config import Config
from models import db, Event

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/name/<name>')
def hello_by_name(name):  # put application's code here
    return f'Hello {name}!'

@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_as_dict = [event.as_dict() for event in events]
    return jsonify(events_as_dict)



if __name__ == '__main__':
    app.run()

from flask import  jsonify,Flask
from config import Config
from models import db, Event
from sqlalchemy import func, and_


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

@app.route('/events/<start_date>/<end_date>', methods=['GET'])
def get_events_by_range(start_date, end_date):
    try:
        cte_date_range = db.session.query(
            Event.id,
            Event.event_date,
            Event.event_name,
            Event.event_address,
            Event.event_desc
        ).filter(
            Event.event_date.between(start_date, end_date)
        ).cte('cte_date_range')

        cte_get_last_update = db.session.query(
            cte_date_range.c.id,
            func.max(cte_date_range.c.event_date).label('latest_update')
        ).group_by(
            cte_date_range.c.id
        ).cte('cte_get_last_update')

        # Main query with join
        events_query = db.session.query(
            Event
        ).join(
            cte_get_last_update,
            and_(
                Event.id == cte_get_last_update.c.id,
                Event.event_date == cte_get_last_update.c.latest_update
            )
        )

        events = events_query.all()

        events_as_dict = [event.as_dict() for event in events]

        return jsonify(events_as_dict)
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        print(error_msg)  
        return jsonify({"error": error_msg}), 500




if __name__ == '__main__':
    app.run()

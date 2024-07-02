from flask import jsonify, Flask, request
from config import Config
from models import db, Event
from sqlalchemy import func, and_
import pandas as pd

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

def fill_default_values(df):
    default_texts = {
        'event_name': 'name not included',
        'event_address': 'address not included',
        'event_desc': 'description not included'
    }

    for column, default_value in default_texts.items():
        df[column] = df[column].apply(lambda x: default_value if isinstance(x, str) and x.strip() == "" else x)

    return df

@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_as_dict = [event.as_dict() for event in events]

    df = pd.DataFrame(events_as_dict)
    df = fill_default_values(df)

    return jsonify(df.to_dict(orient='records'))

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

        df = pd.DataFrame(events_as_dict)
        if len(events_as_dict)>0:
         df = fill_default_values(df)


        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        print(error_msg)
        return jsonify({"error": error_msg}), 500


@app.route('/events/earliest', methods=['GET'])
def get_earliest_event():
    try:
        events = Event.query.all()

        events_as_dict = [event.as_dict() for event in events]

        df = pd.DataFrame(events_as_dict)
        df = fill_default_values(df)

        df_sorted = df.sort_values(by='event_date')

        sorted_events = df_sorted.to_dict(orient='records')

        return jsonify(sorted_events)
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        print(error_msg)
        return jsonify({"error": error_msg}), 500


@app.route('/event/name/<name>', methods=['GET'])
def get_event_by_name(name):
    try:
        events = Event.query.all()

        events_as_dict = [event.as_dict() for event in events]

        df = pd.DataFrame(events_as_dict)
        df = fill_default_values(df)

        filtered_events = df[df["event_name"].str.contains(name, case=False, na=False)]

        filtered_events_dict = filtered_events.to_dict(orient='records')

        return jsonify(filtered_events_dict)
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        print(error_msg)
        return jsonify({"error": error_msg}), 500


@app.route('/event/address/<address>', methods=['GET'])
def get_event_by_address(address):
    try:
        events = Event.query.all()

        events_as_dict = [event.as_dict() for event in events]

        df = pd.DataFrame(events_as_dict)
        df = fill_default_values(df)

        filtered_events = df[df["event_address"].str.contains(address, case=False, na=False)]

        filtered_events_dict = filtered_events.to_dict(orient='records')

        return jsonify(filtered_events_dict)
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        print(error_msg)
        return jsonify({"error": error_msg}), 500


@app.route('/events/latest', methods=['GET'])
def get_latest_event():
    try:
        events = Event.query.all()

        events_as_dict = [event.as_dict() for event in events]

        df = pd.DataFrame(events_as_dict)
        df = fill_default_values(df)

        df_sorted = df.sort_values(by='event_date', ascending=False)

        sorted_events = df_sorted.to_dict(orient='records')

        return jsonify(sorted_events)
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        print(error_msg)
        return jsonify({"error": error_msg}), 500


if __name__ == '__main__':
    app.run()

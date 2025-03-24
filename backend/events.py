from flask import Flask, request, render_template, jsonify,Blueprint
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="bloodlife"
)

cursor = db.cursor()

# Route: Event Search Page

events_bp = Blueprint('events', __name__)

@events_bp.route('/')

def events():
    return render_template('events.html')

# Home Route (Redirects to Event Search Page)
'''@app.route('/')
def home():
    return render_template('events.html')'''

# Route: Fetch Events by Location (API)
@events_bp.route('/get_events', methods=['GET'])
def get_events():
    location = request.args.get('location', '').lower()

    if not location:
        return jsonify({"events": []})

    query = "SELECT name, event_date, location, description FROM events WHERE LOWER(location) LIKE %s"
    cursor.execute(query, ('%' + location + '%',))
    events = cursor.fetchall()

    event_list = [{
        "name": event[0],
        "event_date": event[1].strftime('%Y-%m-%d'),  # Convert date format
        "location": event[2],
        "description": event[3]
    } for event in events]

    return jsonify({"events": event_list})
app.register_blueprint(events_bp, url_prefix='/events')

@app.route('/')
def home():
    return render_template('events.html')


if __name__ == '__main__':
    app.run(debug=True)

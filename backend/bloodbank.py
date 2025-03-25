#FOR Blood_Banks
#fetch
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

bloodbank_bp = Blueprint('bloodbank', __name__)

@bloodbank_bp.route('/')
# Route: Render Blood Bank Locator Page

def bloodbank():
    return render_template('bloodbank.html')

'''@app.route('/')
def home():
    return render_template('bloodbank.html')'''

# Route: Fetch Blood Banks by Location (API)
@bloodbank_bp.route('/get_blood_banks', methods=['GET'])
def get_blood_banks():
    location = request.args.get('location', '').strip().lower()

    if location:  # If location is provided, filter the results
        query = "SELECT name, address, contact FROM blood_banks WHERE LOWER(location) LIKE %s"
        cursor.execute(query, ('%' + location + '%',))
    else:  # If no location is provided, return all blood banks
        query = "SELECT name, address, contact FROM blood_banks"
        cursor.execute(query)

    blood_banks = cursor.fetchall()
    bloodbank_list = [{"name": b[0], "address": b[1], "contact": b[2]} for b in blood_banks]

    return jsonify({"blood_banks": bloodbank_list})
app.register_blueprint(bloodbank_bp, url_prefix='/bloodbank')

@app.route('/')
def home():
    return render_template('events.html')


if __name__ == '__main__':
    app.run(debug=True)
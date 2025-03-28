#For Hospitals
from flask import Flask, request, render_template, jsonify,redirect,url_for,Blueprint
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

# Route: Search Hospitals by Location (HTML Page)

hospital_bp = Blueprint('hospital', __name__)

@hospital_bp.route('/',methods=['GET'])

def hospital():
    return render_template('hospital.html')


'''@app.route('/')
def home():
    return render_template('search_hospital.html')'''
    


# Route: Fetch Hospitals by Location (API)
@hospital_bp.route('/get_hospital',methods=['GET'])
def get_hospital():
    location = request.args.get('location', '').strip().lower()  # Get location input


    try:
        cursor = db.cursor()  # Ensure a new cursor instance
        if location:
            # If location is provided, filter results
            query = "SELECT name, address, contact FROM hospitals WHERE LOWER(location) LIKE %s"
            cursor.execute(query, ('%' + location + '%',))
        else:
            # Fetch all hospitals when no location is provided
            query = "SELECT name, address, contact FROM hospitals"
            cursor.execute(query)

        hospitals = cursor.fetchall()

        hospital_list = [{"name": hospital[0], "address": hospital[1], "contact": hospital[2]} for hospital in hospitals]

        return jsonify({"hospitals": hospital_list})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/')
def home():
    return render_template('hospital.html')

if __name__ == '__main__':
    app.run(debug=True)
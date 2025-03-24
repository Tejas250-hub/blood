from flask import Flask, flash, redirect, url_for, render_template, request, jsonify,Blueprint
from backend.send_email import send_email_to_donor, send_email_to_patient
import mysql.connector


app = Flask(__name__)

# Configure MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="bloodlife"
)


app.secret_key = 'your_secret_key'

# Initialize MySQL


def get_current_max_donor_id():
    """Retrieve the current maximum donor_id from the database."""
    cursor = db.cursor()
    cursor.execute("SELECT COALESCE(MAX(donor_id), 0) FROM donors")  # Use COALESCE to handle empty table
    max_id = cursor.fetchone()[0]
    cursor.close()
    return max_id
donate_bp = Blueprint('donate', __name__)

@donate_bp.route('/donate',methods=['GET'])


def donate():
    # Get the current maximum donor_id and increment it
    current_max_id = get_current_max_donor_id()
    donor_id = current_max_id + 1  # Increment the donor_id
    return render_template('donate.html', donor_id=donor_id)  # Render your HTML form

@donate_bp.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get form data
        full_name = request.form['fullName']
        dob = request.form['dob']
        blood_group = request.form['bloodGroup']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        current_location = request.form['currentLocation']
        # Get available locations (this will be a list)
        available_locations = request.form.getlist('availableLocation')  # Ensure this line is correct
        # Join the list into a single string, separated by commas (or any other delimiter)
        available_location = ', '.join(available_locations)

        # Insert data into MySQL database
        cursor = db.cursor()

        cursor.execute('''INSERT INTO donors (full_name, dob, blood_group, gender, email, phone, current_location, available_location) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', 
                       (full_name, dob, blood_group, gender, email, phone, current_location, available_location))
        db.commit()

        donor_id = cursor.lastrowid
        cursor.close()

        # Redirect to the index route with the donor_id as a query parameter
        return redirect(url_for('donate.donate', donor_id=donor_id))  # Pass donor_id to the index route

    # If the request method is not POST, return an error
    return jsonify({'error': 'Invalid request method.'}), 400


if __name__ == '__main__':
    app.run(debug=True)
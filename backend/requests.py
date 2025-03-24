from flask import Flask, flash, redirect, url_for, render_template, request, jsonify, Blueprint
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


def get_current_max_request_id():
    """Retrieve the current maximum request_id from the database."""
    cursor = db.cursor()
    cursor.execute("SELECT COALESCE(MAX(request_id), 0) FROM request")  
    max_id = cursor.fetchone()[0]
    cursor.close()
    return max_id


# ✅ Create Blueprint
requests_bp = Blueprint('requests', __name__, template_folder='templates')


# ✅ Route to Show Request Form
@requests_bp.route('/requests', methods=['GET', 'POST'])
def requests():
    # Get the current maximum request_id and increment it
    current_max_request_id = get_current_max_request_id()
    request_id = current_max_request_id + 1  
    
    donors = []
    if request.method == 'POST':
        blood_group = request.form.get('blood_group')
        location = request.form.get('location')

        if blood_group and location:
            cursor = db.cursor()
            query = """ 
                SELECT donor_id, full_name, email, blood_group, location, available_locations 
                FROM donors 
                WHERE TRIM(blood_group) = %s 
                AND (location = %s OR FIND_IN_SET(%s, available_locations) > 0)
            """
            cursor.execute(query, (blood_group.strip(), location, location))
            donors = cursor.fetchall()  
            cursor.close()

    # ✅ Render the Request Form
    return render_template('requests.html', request_id=request_id, donors=donors)


# ✅ Route to Handle Form Submission
@requests_bp.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get form data
        patient_name = request.form['patient_name']
        phone = request.form['phone']
        blood_group = request.form['bloodgroup']
        quantity = request.form['quantity']
        email = request.form['email']
        location = request.form['location']
        address = request.form['address']

        # ✅ Insert Request Into Database
        cursor = db.cursor()
        cursor.execute('''INSERT INTO request (patient_name, phone, blood_group, email, quantity, location, address) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                       (patient_name, phone, blood_group, email, quantity, location, address))
        db.commit()
        request_id = cursor.lastrowid

        cursor.execute("INSERT INTO request_status (request_id) VALUES (%s)", (request_id,))
        db.commit()

        # ✅ Fetch Matching Donors
         # Fetch matching donors based on blood group and location
        cursor.execute("""
    SELECT donor_id, full_name, email, blood_group, current_location, available_location 
    FROM donors 
    WHERE TRIM(blood_group) = %s 
    AND (current_location = %s OR available_location LIKE %s)
""", (blood_group.strip(), location, f"%{location}%"))


        donors = cursor.fetchall()
        cursor.close()

        for donor in donors:
            donor_id, full_name, email, blood_group, current_location, available_location = donor
            
            # ✅ Call send_email_to_donor Function
            send_email_to_donor(
                donor_name=full_name,
                donor_email=email,
                patient_name=patient_name,
                blood_group=blood_group,
                hospital=address,
                location=location,
                contact=phone,
                request_id=request_id,
                donor_id=donor_id
            )

        flash("✅ Blood Request Submitted and Emails Sent Successfully!")

        # ✅ Render Template with Donors
        return render_template('requests.html', request_id=request_id, donors=donors)

    return jsonify({'error': 'Invalid request method.'}), 400

@requests_bp.route('/accept_request')
def accept_request():
    request_id = request.args.get('id')
    donor_id = request.args.get('donor_id')

    cursor = db.cursor()

    # ✅ Update the request_status table to mark as accepted
    cursor.execute("""
        UPDATE request_status SET accepted=1, pending=0, declined=0
        WHERE request_id=%s AND donor_id=%s
    """, (request_id, donor_id))
    db.commit()

    # ✅ Fetch Donor Details
    cursor.execute("SELECT full_name, phone, email FROM donors WHERE donor_id=%s", (donor_id,))
    donor = cursor.fetchone()
    if not donor:
        flash("❌ Donor not found!", "danger")
        return redirect(url_for('requests.requests'))

    donor_name, donor_phone, donor_email = donor

    # ✅ Fetch Patient Email
    cursor.execute("SELECT email FROM request WHERE request_id=%s", (request_id,))
    patient = cursor.fetchone()
    if not patient:
        flash("❌ Patient email not found!", "danger")
        return redirect(url_for('requests.requests'))

    patient_email = patient[0]

    # ✅ Send Email to Patient with Donor Details
    send_email_to_patient(patient_email, donor_name, donor_phone, donor_email)

    flash("✅ Donor details sent to the patient successfully!", "success")
    return redirect(url_for('requests.requests'))


# ✅ Route to Handle Decline Request
@requests_bp.route('/decline_request')
def decline_request():
    request_id = request.args.get('id')
    donor_id = request.args.get('donor_id')

    if not request_id or not donor_id:
        flash("Invalid request ID or donor ID")
        return redirect(url_for('requests.requests'))

    cursor = db.cursor()

    # ✅ Ensure the request exists
    cursor.execute("SELECT * FROM request_status WHERE request_id = %s", (request_id,))
    request_exists = cursor.fetchone()

    if not request_exists:
        flash("Request not found!")
        return redirect(url_for('requests.requests'))

    # ✅ Update request_status table: Mark as declined
    cursor.execute("""
        UPDATE request_status 
        SET declined = 1, accepted = 0, pending = 0
        WHERE request_id = %s
    """, (request_id,))
    db.commit()

    return f"Request is being decilned"



# ✅ Register Blueprint with URL Prefix
app.register_blueprint(requests_bp, url_prefix='/requests')

if __name__ == '__main__':
    app.run(debug=True)

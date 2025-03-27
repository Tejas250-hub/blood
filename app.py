from flask import Flask,render_template,request,flash
import mysql.connector
#from FinalyearProj.admin import admin_bp
from backend.donate import donate_bp
from backend.bloodbank import bloodbank_bp
from backend.events import events_bp
from backend.hospital import hospital_bp
from backend.requests import requests_bp
from backend.send_email import  send_email_to_patient
#commit
# Configure MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="bloodlife"
)
app = Flask(__name__)

app.secret_key = "a47734f71ca28674ed2e5868cd21af8e"

# Register Blueprints (Routes)
#app.register_blueprint(admin_bp,url_prefix='/admin')
app.register_blueprint(donate_bp,url_prefix='/donate')
app.register_blueprint(bloodbank_bp,url_prefix='/bloodbank')
app.register_blueprint(events_bp,url_prefix='/events')
app.register_blueprint(hospital_bp,url_prefix='/hospital')
app.register_blueprint(requests_bp,url_prefix='/requests')


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/accept_request")
def accept_request():
    request_id = request.args.get("id")
    donor_id = request.args.get("donor_id")
    cursor = db.cursor()

    # ✅ Update request_status to 'Accepted'
    cursor.execute("""
        UPDATE request_status SET accepted=1, declined=0, pending=0
        WHERE request_id=%s
    """, (request_id,))
    db.commit()
    # ✅ Fetch Donor Details
    cursor.execute("SELECT full_name, phone, email FROM donors WHERE donor_id=%s", (donor_id,))
    donor = cursor.fetchone()
    if not donor:
        flash("❌ Donor not found!", "danger")
        

    donor_name, donor_phone, donor_email = donor

    # ✅ Fetch Patient Email
    cursor.execute("SELECT email FROM request WHERE request_id=%s", (request_id,))
    patient = cursor.fetchone()
    if not patient:
        flash("❌ Patient email not found!", "danger")
        

    patient_email = patient[0]

    print(f"Donor Details: Name={donor_name}, Phone={donor_phone}, Email={donor_email}")
    print(f"Patient Email: {patient_email}")

    # ✅ Send Email to Patient with Donor Details
    send_email_to_patient(patient_email, donor_name, donor_phone, donor_email)

    flash("✅ Donor details sent to the patient successfully!", "success")
   

    
    
    if not request_id or not donor_id:
        return "Invalid request. Missing parameters.", 400

    # Update the database to mark the request as accepted
    # Example: update_request_status(request_id, donor_id, "Accepted")

    return f"✅ Blood donation request {request_id} accepted by donor {donor_id}."



@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')



if __name__ == '__main__':
    app.run(debug=True)

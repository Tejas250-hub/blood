import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os  # For environment variables

# Load email credentials from environment variables (recommended)
SENDER_EMAIL = os.getenv("EMAIL_USER", "tejashree798@gmail.com")  # Replace with your email
SENDER_PASSWORD = os.getenv("EMAIL_PASS", "yqfp zjmi syxe oinf")  # Use App Password

# ✅ Function to Send Email to Donor
def send_email_to_donor(donor_name, donor_email, patient_name, blood_group, hospital, location, contact, request_id, donor_id):
    subject = f"Blood Donation Request for {blood_group} Blood"

    body = f"""
    <html>
    <body>
        <h2>Blood Donation Request</h2>
        <p><b>Dear {donor_name},</b></p>
        <p>A patient needs your help. Below are the details:</p>
        <table border='1' cellspacing='0' cellpadding='10'>
            <tr><td><b>Patient Name:</b></td><td>{patient_name}</td></tr>
            <tr><td><b>Blood Group:</b></td><td>{blood_group}</td></tr>
            <tr><td><b>Hospital Name:</b></td><td>{hospital}</td></tr>
            <tr><td><b>Location:</b></td><td>{location}</td></tr>
            <tr><td><b>Contact Number:</b></td><td>{contact}</td></tr>
        </table>
        <br>
        <p>Please click on one of the below options:</p>
        <a href="http://localhost:5000/accept_request?id={request_id}&donor_id={donor_id}" 
           style="background-color:green; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;">
           ✅ Accept Request
        </a>
        &nbsp;&nbsp;&nbsp;
        <a href="http://localhost:5000/requests/decline_request?id={request_id}&donor_id={donor_id}" 
           style="background-color:red; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;">
           ❌ Decline Request
        </a>
        <br><br>
        <p>Thank you for supporting our Blood Donation Drive!</p>
    </body>
    </html>
    """

    send_email(donor_email, subject, body)
    print(f"✅ Email sent to {donor_email}")

# ✅ Function to Send Email to Patient
def send_email_to_patient(patient_email, donor_name, donor_phone, donor_email):
    subject = "Donor Contact Details for Your Blood Request"
    body = f"""
    <html>
    <body>
        <h2>Blood Donor Contact Details</h2>
        <p><b>Dear Patient,</b></p>
        <p>The following donor has accepted your blood donation request. Please contact the donor as soon as possible.</p>
        <table border='1' cellspacing='0' cellpadding='10'>
            <tr><td><b>Donor Name:</b></td><td>{donor_name}</td></tr>
            <tr><td><b>Donor Phone:</b></td><td>{donor_phone}</td></tr>
            <tr><td><b>Donor Email:</b></td><td>{donor_email}</td></tr>
        </table>
        <br>
        <p>Please coordinate with the donor to arrange for blood donation.</p>
        <p><b>Thank you for using our Blood Bank Service.</b></p>
    </body>
    </html>
    """

    send_email(patient_email, subject, body)
    print("✅ Donor Contact Sent to Patient")

# ✅ Common Email Sending Function
def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"✅ Email successfully sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

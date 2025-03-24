from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management

# Dummy admin login credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# ✅ Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",  # Set your MySQL password
        database="bloodlife"
    )

# ================================
# 🛡️ Admin Routes
# ================================

# ✅ Home Route - Admin Panel
@app.route('/')
def home():
    return render_template('admin_login.html')

# ✅ Admin Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_panel"))
        else:
            return render_template("admin_login.html", error="Invalid credentials")

    return render_template("admin_login.html")

# ✅ Admin Panel Route
@app.route("/admin_panel")
def admin_panel():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    return render_template("admin_panel.html")


# ✅ Admin Logout
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("login"))

# ================================
# 🩸 Blood Bank Management Routes
# ================================

# ✅ Add Blood Bank
@app.route('/add_bloodbank', methods=['POST'])
def add_bloodbank():
    name = request.form.get('name')
    contact = request.form.get('contact')
    address = request.form.get('address')
    location = request.form.get('location')

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO blood_banks (name, contact, address, location) VALUES (%s, %s, %s, %s)",
        (name, contact, address, location),
    )
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Blood Bank added successfully!"})

# ✅ Get All Blood Banks
@app.route('/get_bloodbank', methods=['GET'])
def get_bloodbank():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM blood_banks")
    blood_banks = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(blood_banks)

# ✅ Get Blood Bank by ID
@app.route('/get_bloodbank_by_id/<int:id>', methods=['GET'])
def get_bloodbank_by_id(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM blood_banks WHERE id = %s", (id,))
    bloodbank = cursor.fetchone()
    cursor.close()
    connection.close()

    if bloodbank:
        return jsonify(bloodbank)
    else:
        return jsonify({"error": "Blood Bank not found"}), 404

# ✅ Update Blood Bank by ID
@app.route('/update_bloodbank/<int:id>', methods=['PUT'])
def update_bloodbank(id):
    data = request.json
    name = data.get('name')
    contact = data.get('contact')
    address = data.get('address')
    location = data.get('location')

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE blood_banks
        SET name = %s, contact = %s, address = %s, location = %s
        WHERE id = %s
        """,
        (name, contact, address, location, id),
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Blood Bank updated successfully!"})

# ✅ Delete Blood Bank by ID
@app.route('/delete_bloodbank/<int:id>', methods=['DELETE'])
def delete_bloodbank(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM blood_banks WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Blood Bank deleted successfully!"})

# ================================
# 🏥 Hospital Management Routes
# ================================

# ✅ Add Hospital
@app.route('/add_hospital', methods=['POST'])
def add_hospital():
    name = request.form.get('name')
    contact = request.form.get('contact')
    address = request.form.get('address')
    location = request.form.get('location')

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO hospitals (name, contact, address, location) VALUES (%s, %s, %s, %s)",
        (name, contact, address, location),
    )
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Hospital added successfully!"})

# ✅ Get All Hospitals
@app.route('/get_hospitals', methods=['GET'])
def get_hospitals():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM hospitals")
    hospitals = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(hospitals)

# ✅ Update Hospital by ID
@app.route('/update_hospital/<int:id>', methods=['PUT'])
def update_hospital(id):
    data = request.json
    name = data.get('name')
    contact = data.get('contact')
    address = data.get('address')
    location = data.get('location')

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE hospitals
        SET name = %s, contact = %s, address = %s, location = %s
        WHERE id = %s
        """,
        (name, contact, address, location, id),
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Hospital updated successfully!"})

# ✅ Delete Hospital by ID
@app.route('/delete_hospital/<int:id>', methods=['DELETE'])
def delete_hospital(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM hospitals WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Hospital deleted successfully!"})

# ================================
# 🎉 Event Management Routes
# ================================

# ✅ Add Event
@app.route('/add_event', methods=['POST'])
def add_event():
    name = request.form.get('name')
    event_date = request.form.get('event_date')
    location = request.form.get('location')
    description = request.form.get('description')

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO events (name, event_date, location, description) VALUES (%s, %s, %s, %s)",
        (name, event_date, location, description),
    )
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Event added successfully!"})

# ✅ Get All Events
@app.route('/get_events', methods=['GET'])
def get_events():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(events)


# ✅ Update Event by ID
@app.route('/update_event/<int:id>', methods=['PUT'])
def update_event(id):

    data = request.json
    name = data.get('name')
    event_date = data.get('event_date')
    location = data.get('location')
    description = data.get('description')

    # ❌ Wrong - Remove this
    # conn = mysql.connection
    # cursor = conn.cursor()

    # ✅ Correct - Use get_db_connection()
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
            UPDATE events
            SET name = %s, event_date = %s, location = %s, description = %s
            WHERE id = %s
        """, (name, event_date, location, description, id))

    connection.commit()
    cursor.close()
    connection.close()
        
    return jsonify({"message": "Event updated successfully!"})
    



    
# ✅ Delete Event by ID
@app.route('/delete_event/<int:id>', methods=['DELETE'])
def delete_event(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM events WHERE id = %s", (id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Event not found"}), 404

        cursor.close()
        conn.close()
        return jsonify({"message": "Event deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================================
# 🚀 Run Flask Application
# ================================

@app.route('/delete_<section>/<int:id>', methods=['DELETE'])
def delete_entry(section, id):
    table_mapping = {
        "event": "events",
        "hospitals": "hospitals",
        "bloodbank": "blood_banks"
    }
    table_name = table_mapping.get(section)
    
    if not table_name:
        return jsonify({"message": "Invalid section"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (id,))
    connection.commit()

    if cursor.rowcount:
        message = f"{section.capitalize()} deleted successfully!"
    else:
        message = f"{section.capitalize()} not found."

    cursor.close()
    connection.close()

    return jsonify({"message": message})

@app.route('/get_<section>_by_id/<int:id>', methods=['GET'])
def get_entry_by_id(section, id):
    table_mapping = {
        "events": "events",
        "hospitals": "hospitals",
        "bloodbank": "blood_banks"
    }
    
    table_name = table_mapping.get(section)
    if not table_name:
        return jsonify({"message": "Invalid section"}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result:
        return jsonify(result)
    else:
        return jsonify({"message": f"{section.capitalize()} not found"}), 404


@app.route('/update_<section>/<int:id>', methods=['PUT'])
def update_entry(section, id):
    table_mapping = {
        "events": "events",
        "hospitals": "hospitals",
        "bloodbank": "blood_banks"
    }
    
    table_name = table_mapping.get(section)
    if not table_name:
        return jsonify({"message": "Invalid section"}), 400

    data = request.json
    
    if not data:
        return jsonify({"message": "No data provided"}), 400

    # Build dynamic update query
    update_fields = []
    values = []

    for key, value in data.items():
        update_fields.append(f"{key} = %s")
        values.append(value)

    values.append(id)

    query = f"UPDATE {table_name} SET {', '.join(update_fields)} WHERE id = %s"

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(query, tuple(values))
    connection.commit()

    if cursor.rowcount:
        message = f"{section.capitalize()} updated successfully!"
    else:
        message = f"No changes made to {section}."

    cursor.close()
    connection.close()

    return jsonify({"message": message})

@app.route('/get_donors', methods=['GET'])
def get_donors():
    connection = get_db_connection()  # Corrected DB connection
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM donors")  # Assuming 'donors' is the correct table
    donors = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return jsonify(donors)


@app.route('/get_bloodRequests', methods=['GET'])
def get_blood_requests():
    print("Fetching blood requests...")  # Debug
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM request")  # Ensure table name is correct
    blood_requests = cursor.fetchall()

    print("Data fetched:", blood_requests)  # Check if data is returned
    cursor.close()
    connection.close()

    if blood_requests:
        return jsonify(blood_requests)
    else:
        print("No blood requests found!")
        return jsonify({"message": "No blood requests found"}), 404


@app.route('/get_request_status', methods=['GET'])
def get_request_status():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT request_id, accepted, declined, pending FROM request_status")
    request_status = cursor.fetchall()
    cursor.close()
    return jsonify(request_status)

if __name__ == '__main__':
    app.run(debug=True)
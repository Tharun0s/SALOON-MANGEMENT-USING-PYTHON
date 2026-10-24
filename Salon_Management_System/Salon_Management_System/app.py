from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Change these values to match your MySQL setup.
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456789",  # Add your MySQL password here
    "database": "salon_db"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/services", methods=["GET"])
def services():
    return jsonify([
        {"name": "Hair Cut", "price": 150},
        {"name": "Hair Styling", "price": 250},
        {"name": "Beard Trim", "price": 100},
        {"name": "Hair Coloring", "price": 500},
        {"name": "Facial", "price": 400}
    ])

@app.route("/api/appointments", methods=["GET", "POST"])
def appointments():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        name = data.get("name", "").strip()
        phone = data.get("phone", "").strip()
        service = data.get("service", "").strip()
        date = data.get("date", "").strip()
        time = data.get("time", "").strip()

        if not all([name, phone, service, date, time]):
            return jsonify({"error": "Please fill in all fields."}), 400

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO appointments
                   (customer_name, phone, service, appointment_date, appointment_time)
                   VALUES (%s, %s, %s, %s, %s)""",
                (name, phone, service, date, time)
            )
            conn.commit()
            new_id = cursor.lastrowid
            cursor.close()
            conn.close()
            return jsonify({"message": "Appointment booked successfully!", "id": new_id}), 201
        except Error as e:
            return jsonify({"error": "Database connection failed. Check MySQL setup and schema.sql."}), 500

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT id, customer_name, phone, service,
                          appointment_date, appointment_time, created_at
                          FROM appointments ORDER BY id DESC""")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for row in rows:
            row["appointment_date"] = str(row["appointment_date"])
            row["appointment_time"] = str(row["appointment_time"])
            row["created_at"] = str(row["created_at"])
        return jsonify(rows)
    except Error:
        return jsonify({"error": "Could not load appointments. Check MySQL setup."}), 500

@app.route("/api/appointments/<int:appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
        conn.commit()
        deleted = cursor.rowcount
        cursor.close()
        conn.close()
        if not deleted:
            return jsonify({"error": "Appointment not found."}), 404
        return jsonify({"message": "Appointment deleted."})
    except Error:
        return jsonify({"error": "Could not delete appointment. Check MySQL setup."}), 500

if __name__ == "__main__":
    app.run(debug=True)

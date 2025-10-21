from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_mysql_password",
    database="hospital_db"
)

@app.route('/')
def home():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.appointment_id, p.name AS patient, d.name AS doctor, 
               a.appointment_date, a.notes
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        ORDER BY a.appointment_date DESC
    """)
    appointments = cursor.fetchall()
    return render_template('index.html', appointments=appointments)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
import os
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    port=int(os.getenv('DB_PORT'))
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

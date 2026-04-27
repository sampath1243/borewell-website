from flask import Flask, render_template, request, redirect, jsonify, session, url_for
import sqlite3
import razorpay
import os
from flask_cors import CORS
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey123"
CORS(app)

# Razorpay setup
client = razorpay.Client(auth=(os.getenv("RAZORPAY_KEY"), os.getenv("RAZORPAY_SECRET")))

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# ---------------- DB ----------------
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            drilling_type TEXT,
            rigs INTEGER,
            feet INTEGER,
            work_type TEXT,
            location TEXT,
            date TEXT,
            advance INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTES ----------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

# ---------------- SUBMIT ----------------
@app.route('/submit', methods=['POST'])
def submit():
    data = (
        request.form['name'],
        request.form['phone'],
        request.form['drilling_type'],
        request.form['rigs'],
        request.form['feet'],
        request.form['work_type'],
        request.form['location'],
        request.form['date'],
        request.form.get('advance', 0)
    )

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings 
        (name, phone, drilling_type, rigs, feet, work_type, location, date, advance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

    # WhatsApp message
    message = f"Hello {data[0]}, your borewell booking is confirmed!"
    whatsapp_url = f"https://wa.me/{data[1]}?text={urllib.parse.quote(message)}"

    return redirect(whatsapp_url)

# ---------------- ADMIN LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USERNAME and request.form['password'] == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/admin')
        return "Invalid Login"

    return render_template('login.html')

# ---------------- ADMIN ----------------
@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    data = cursor.fetchall()
    conn.close()

    return render_template('admin.html', data=data)

# ---------------- PAYMENT ----------------
@app.route('/create-order', methods=['POST'])
def create_order():
    amount = int(request.json['amount']) * 100

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return jsonify(order)

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
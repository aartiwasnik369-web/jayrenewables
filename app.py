from flask import Flask, render_template, request, redirect, session
import sqlite3
import smtplib

app = Flask(__name__)
app.secret_key = "secret123"

ADMIN_USER = "Dr. Jay"
ADMIN_PASS = "1@2#3$"

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS enquiries(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        message TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- CONTACT FORM ----------------
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form["name"]
    phone = request.form["phone"]
    message = request.form["message"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO enquiries(name,phone,message) VALUES (?,?,?)",
                (name, phone, message))
    conn.commit()
    conn.close()

    # -------- EMAIL SEND --------
    try:
        sender = "YOUR_EMAIL@gmail.com"
        password = "EMAIL_APP_PASSWORD"
        receiver = "YOUR_EMAIL@gmail.com"

        body = f"New enquiry\nName:{name}\nPhone:{phone}\nMessage:{message}"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, body)
        server.quit()
    except:
        print("Email not sent")

    return redirect("/")

# ---------------- ADMIN LOGIN ----------------
@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USER and request.form["password"] == ADMIN_PASS:
            session["admin"] = True
            return redirect("/dashboard")
    return render_template("admin_login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/admin")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    data = cur.execute("SELECT * FROM enquiries").fetchall()
    conn.close()

    return render_template("admin_dashboard.html", data=data)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/admin")

app.run(debug=True)
from flask import Flask, render_template, request, redirect, jsonify, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ---------------- DATABASE INIT ----------------
def init_db():
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    name = request.form.get("Name")
    email = request.form.get("Email")
    message = request.form.get("Message")

    if not name or not email or not message:
        flash("All fields are required")
        return redirect("/")

    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages(name,email,message) VALUES (?,?,?)",
        (name, email, message)
    )

    conn.commit()
    conn.close()

    flash("Message sent successfully!")
    return redirect("/")

# ---------------- API ----------------
@app.route("/api/messages")
def api_messages():
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM messages")
    rows = cursor.fetchall()

    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "message": row[3],
            "created_at": row[4]
        })

    return jsonify(result)

# ---------------- AUTH ----------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["user"] = username
            return redirect("/admin")
        else:
            flash("Invalid credentials")
            return redirect("/login")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect("/login")
    return render_template("admin.html")

# ---------------- DELETE ----------------
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return "Deleted"

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
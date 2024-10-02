from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)



# Create the database and table if they don't exist

# SQLite setup
conn = sqlite3.connect('/var/www/html/flaskapp/users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (username TEXT, password TEXT, firstname TEXT, lastname TEXT, email TEXT)''')
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']

    conn = sqlite3.connect('/var/www/html/flaskapp/users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, firstname, lastname, email) VALUES (?, ?, ?, ?, ?)",
              (username, password, firstname, lastname, email))
    
    conn.commit()
    conn.close()

    return redirect(url_for('profile', username=username))

@app.route('/profile/<username>')
def profile(username):
    conn = sqlite3.connect('/var/www/html/flaskapp/users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    return render_template('profile.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('/var/www/html/flaskapp/users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        
        if user:            
            return redirect(url_for('profile', username=username))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

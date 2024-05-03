from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('register_form'))

@app.route('/register', methods=['GET'])
def register_form():
    # Show the registration form
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username'].strip().lower()  # Normalize username to lowercase and strip whitespace
    email = request.form['email'].strip()
    password = request.form['password'].strip()

    # Check if username already exists
    with open('registrations.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'].strip().lower() == username:
                return render_template('register.html', error='Username already exists')  # Return an error message

    # Save the data to a CSV file
    with open('registrations.csv', 'a', newline='') as csvfile:
        fieldnames = ['username', 'email', 'password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvfile.seek(0, 2)  # Move to the end of the file
        if csvfile.tell() == 0:
            writer.writeheader()  # Write header only once
        writer.writerow({'username': username, 'email': email, 'password': password})

    return redirect(url_for('login_form'))

@app.route('/login', methods=['GET'])
def login_form():
    # Show the login form
    return render_template('login.html')

@app.route('/preview',methods=['GET'])
def preview_form():
    return render_template('preview.html')  # Assume you have a preview.html template

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip().lower()  # Normalize to lowercase and strip whitespace
    password = request.form.get('password', '').strip()

    if not username or not password:
        return render_template('login.html', error='Missing username or password')

    # Check credentials
    valid_login = False
    with open('registrations.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'].strip().lower() == username and row['password'].strip() == password:
                valid_login = True
                break

    if valid_login:
        return redirect(url_for('preview_form'))
    else:
        return render_template('login.html', error='Invalid credentials.')

if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask import jsonify
import bcrypt
import qrcode
import os


app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'chainharbor'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Set a secret key for session management
app.secret_key = 'omen'

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Fetch user details from the form
        user_role = request.form['user_role']
        username = request.form['username']
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        email = request.form['email']
        full_name = request.form['full_name']
        phone_number = request.form['phone_number']
        address = request.form['address']

        # Insert user data into the database
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO users (user_role, username, password, email, full_name, phone_number, address) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (user_role, username, password, email, full_name, phone_number, address)
        )
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('login'))

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password'].encode('utf-8')

        cursor = mysql.connection.cursor()
        result = cursor.execute('SELECT * FROM users WHERE username = %s', [username])

        if result > 0:
            user = cursor.fetchone()
            if bcrypt.checkpw(password_candidate, user['password'].encode('utf-8')):
                # Password matched, create session
                session['user_id'] = user['user_id']
                session['username'] = user['username']

                # Redirect to the appropriate dashboard based on the user's role
                if user['user_role'] == 'farmer':
                    return redirect(url_for('farmer_dashboard'))
                elif user['user_role'] == 'distributor':
                    return redirect(url_for('distributor_dashboard'))
                elif user['user_role'] == 'retailer':
                    return redirect(url_for('retailer_dashboard'))
                elif user['user_role'] == 'consumer':
                    return redirect(url_for('consumer_dashboard'))

            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

        cursor.close()

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Sample route for the farmer's dashboard
@app.route('/farmer_dashboard')
def farmer_dashboard():
    # Assume user is authenticated and has the 'farmer' role
    # Fetch registered batches for the current farmer
    user_id = get_current_user_id()  # Implement this function based on your authentication logic
    registered_batches = fetch_registered_batches(user_id)

    return render_template('farmer_dashboard.html', registered_batches=registered_batches)

@app.route('/distributor_dashboard')
def distributor_dashboard():
    return render_template('distributor_dashboard.html')

# Update the '/register_batch' route
@app.route('/register_batch', methods=['POST'])
def register_batch():
    if request.method == 'POST':
        # Assume user is authenticated and has the 'farmer' role
        # Retrieve form data
        batch_name = request.form['batch_name']
        crop_type = request.form['crop_type']
        quantity = int(request.form['quantity'])
        variety = request.form['variety']
        growing_practices = request.form['growing_practices']
        soil_conditions = request.form['soil_conditions']
        fertilization_methods = request.form['fertilization_methods']
        pest_control_measures = request.form['pest_control_measures']
        harvest_datetime = request.form['harvest_datetime']
        farm_location = request.form['farm_location']
        irrigation_methods = request.form['irrigation_methods']
        weather_conditions = request.form['weather_conditions']
        certifications = request.form['certifications']
        farm_media_path = request.form['farm_media_path']
                       
                       

        # Fetch the current farmer's ID (which is the user_id)
        user_id = get_current_user_id()  # Implement this function based on your authentication logic

        # Insert the new batch into the database and get the generated batch ID
        batch_id = insert_new_batch(user_id, batch_name, crop_type, quantity,
                            variety, growing_practices, soil_conditions,
                            fertilization_methods, pest_control_measures,
                            harvest_datetime, farm_location,
                            irrigation_methods, weather_conditions,
                            certifications, farm_media_path)


        if batch_id:
            # Generate a unique QR code data (using batch ID as data)
            qr_data = f"{batch_id}"

            # Generate a unique filename for the QR code image using batch ID
            qr_filename = f"static/qrcodes/{batch_id}_qr.png"

            # Save the QR code image to the filesystem
            generate_qr_code(qr_data, qr_filename)

            # Update the database with the QR code image path
            update_qr_code_path(batch_id, qr_filename)

    return redirect(url_for('farmer_dashboard'))

# Sample function to fetch registered batches for a farmer
def fetch_registered_batches(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM batches WHERE user_id = %s", (user_id,))
    registered_batches = cur.fetchall()
    cur.close()
    return registered_batches

# Sample function to insert a new batch into the database and get the generated batch ID
def insert_new_batch(user_id, batch_name, crop_type, quantity,
                            variety, growing_practices, soil_conditions,
                            fertilization_methods, pest_control_measures,
                            harvest_datetime, farm_location,
                            irrigation_methods, weather_conditions,
                            certifications, farm_media_path):
    cur = mysql.connection.cursor()
    cur.execute(
    "INSERT INTO batches (user_id, batch_name, crop_type, quantity, date_registered, variety, growing_practices, soil_conditions, fertilization_methods, pest_control_measures, harvest_datetime, farm_location, irrigation_methods, weather_conditions, certifications, farm_media_path) VALUES (%s, %s, %s, %s, CURDATE(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    (user_id, batch_name, crop_type, quantity, variety, growing_practices, soil_conditions, fertilization_methods, pest_control_measures, harvest_datetime, farm_location, irrigation_methods, weather_conditions, certifications, farm_media_path)
)

    mysql.connection.commit()
    batch_id = cur.lastrowid  # Get the generated batch ID
    cur.close()
    return batch_id

# Sample function to update the QR code image path in the database
def update_qr_code_path(batch_id, qr_filename):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE batches SET qr_code_path = %s WHERE batch_id = %s", (qr_filename, batch_id))
    mysql.connection.commit()
    cur.close()

# Sample function to generate QR code and save it as an image
def generate_qr_code(data, filename):
    # Extract the directory path from the filename
    directory = os.path.dirname(filename)

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add the data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Generate the QR code image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image to the specified filename
    img.save(filename)

def get_current_user_id():
    # Replace this with your authentication logic
    # For simplicity, returning user ID from the session
    return session.get('user_id')

if __name__ == '__main__':
 app.run(debug=True)

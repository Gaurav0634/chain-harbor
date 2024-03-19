# Install the required libraries if you haven't already:
# pip install opencv-python-headless pyzbar mysql-connector-python

import cv2
from pyzbar.pyzbar import decode
import mysql.connector
from mysql.connector import Error
import webbrowser

def get_batch_info(batch_id):
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='chainharbor'
        )

        # Execute the query to fetch batch information
        query = f"SELECT * FROM batches WHERE batch_id = {batch_id}"
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                return result
            else:
                return None

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        if connection.is_connected():
            connection.close()

def create_html_popup(info):
    # Create an HTML file with the batch information and styling
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Batch Information</title>
        <style>
            body {{
                font-family: 'Poppins', sans-serif;
                background-color: #B2DFDB;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}

            .container {{
                background-color: #FFFFFF;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                overflow: hidden;
                width: 300px;
                max-width: 100%;
                margin-top: 100px;
            }}

            .header {{
                background-color: #004D40;
                color: #FFFFFF;
                padding: 20px;
                text-align: center;
                margin-top: 0;
            }}

            .form-container {{
                padding: 20px;
            }}

            label {{
                display: block;
                margin-bottom: 8px;
                color: #37474F;
            }}

            p {{
                color: #37474F;
            }}

            .link {{
                text-align: center;
                margin-top: 16px;
            }}

            .link a {{
                color: #004D40;
            }}

            .link a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>

    <body>
        <div class="container">
            <div class="header">
                <h2>Product Tracking</h2>
            </div>
            <div class="form-container">
                <label><strong>Batch ID:</strong> {info[0]}</label>
<label><strong>Batch Name:</strong> {info[2]}</label>
<label><strong>Crop Type:</strong> {info[3]}</label>
<label><strong>Quantity:</strong> {info[4]}</label>
<label><strong>Date Registered:</strong> {info[5]}</label>

<!-- New fields -->
<label><strong>Variety:</strong> {info[7]}</label>
<label><strong>Growing Practices:</strong> {info[8]}</label>
<label><strong>Soil Conditions:</strong> {info[9]}</label>
<label><strong>Fertilization Methods:</strong> {info[10]}</label>
<label><strong>Pest Control Measures:</strong> {info[11]}</label>
<label><strong>Harvest Date and Time:</strong> {info[12]}</label>
<label><strong>Farm Location:</strong> {info[13]}</label>
<label><strong>Irrigation Methods:</strong> {info[14]}</label>
<label><strong>Weather Conditions:</strong> {info[15]}</label>
<label><strong>Certifications:</strong> {info[16]}</label>
<label><strong>Farm Media Path:</strong> {info[17]}</label>


                <div class="link">
                    <p>Back to <a href="#" onclick="window.close();">Scanner</a></p>
                </div>
            </div>
        </div>
    </body>

    </html>
    """

    with open('batch_info.html', 'w') as f:
        f.write(html_content)

    # Open the HTML file in the default web browser
    webbrowser.open('batch_info.html')

def scan_qr_code():
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Decode QR codes in the frame
        decoded_objects = decode(frame)

        for obj in decoded_objects:
            # Extract the data from the QR code (assuming it's the batch_id)
            batch_id = int(obj.data.decode('utf-8'))

            # Fetch batch information from the database
            batch_info = get_batch_info(batch_id)

            if batch_info:
                print(f"Batch Information: {batch_info}")

                # Create an HTML popup window with batch information
                create_html_popup(batch_info)

            else:
                print(f"Batch with ID {batch_id} not found in the database.")

            # Stop scanning after decoding the QR code
            return

        # Display the frame
        cv2.imshow("QR Code Scanner", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_qr_code()

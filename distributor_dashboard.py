

# Install the required libraries if you haven't already:
# pip install opencv-python-headless pyzbar mysql-connector-python

import cv2
from pyzbar.pyzbar import decode
import mysql.connector
from mysql.connector import Error
import webbrowser
from flask import Flask, request, jsonify

app = Flask(__name__)

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

<label><strong>Receipt Date and Time:</strong> <input type="datetime-local" id="receipt_datetime" name="receipt_datetime" required></label>
<label><strong>Transportation Details:</strong> <input type="text" id="transportation_details" name="transportation_details" required></label>
<label><strong>Storage Conditions:</strong> <input type="text" id="storage_conditions" name="storage_conditions" required></label>
<label><strong>Received Quantity:</strong> <input type="number" id="received_quantity" name="received_quantity" required></label>
<label><strong>Incidents and Deviations:</strong> <textarea id="incidents_and_deviations" name="incidents_and_deviations" rows="4" required></textarea></label>
<label><strong>Handling Procedures:</strong> <textarea id="handling_procedures" name="handling_procedures" rows="4" required></textarea></label>
<label><strong>Warehouse Details:</strong> <input type="text" id="warehouse_details" name="warehouse_details" required></label>
<label><strong>Warehouse Conditions:</strong> <input type="text" id="warehouse_conditions" name="warehouse_conditions" required></label>
<label><strong>Distributor Media Path:</strong> <input type="text" id="distributor_media_path" name="distributor_media_path" required></label>
<label><strong>Quality Check Results:</strong> <input type="text" id="quality_check_results" name="quality_check_results" required></label>
<label><strong>Certifications at Checkpoint:</strong> <input type="text" id="certifications_at_checkpoint" name="certifications_at_checkpoint" required></label>
<label><strong>Testing Methods Used:</strong> <input type="text" id="testing_methods_used" name="testing_methods_used" required></label>
<label><strong>Corrective Actions:</strong> <textarea id="corrective_actions" name="corrective_actions" rows="4" required></textarea></label>
<label><strong>Checkpoint Media Path:</strong> <input type="text" id="checkpoint_media_path" name="checkpoint_media_path" required></label>
<label><strong>Timestamp:</strong> <input type="datetime-local" id="timestamp" name="timestamp" required></label>

        <button onclick="saveData()">Save</button>


                <div class="link">
                    <p>Back to <a href="#" onclick="window.close();">Scanner</a></p>
                </div>
            </div>
        </div>
<script>
    function saveData() {
        // Retrieve values from form fields
        var receiptDatetime = document.getElementById('receipt_datetime').value;
        var transportationDetails = document.getElementById('transportation_details').value;
        var storageConditions = document.getElementById('storage_conditions').value;
        var receivedQuantity = document.getElementById('received_quantity').value;
        var incidentsAndDeviations = document.getElementById('incidents_and_deviations').value;
        var handlingProcedures = document.getElementById('handling_procedures').value;
        var warehouseDetails = document.getElementById('warehouse_details').value;
        var warehouseConditions = document.getElementById('warehouse_conditions').value;
        var distributorMediaPath = document.getElementById('distributor_media_path').value;
        var qualityCheckResults = document.getElementById('quality_check_results').value;
        var certificationsAtCheckpoint = document.getElementById('certifications_at_checkpoint').value;
        var testingMethodsUsed = document.getElementById('testing_methods_used').value;
        var correctiveActions = document.getElementById('corrective_actions').value;
        var checkpointMediaPath = document.getElementById('checkpoint_media_path').value;
        var timestamp = document.getElementById('timestamp').value;

        // Prepare data object to send to the server
        var data = {
            receipt_datetime: receiptDatetime,
            transportation_details: transportationDetails,
            storage_conditions: storageConditions,
            received_quantity: receivedQuantity,
            incidents_and_deviations: incidentsAndDeviations,
            handling_procedures: handlingProcedures,
            warehouse_details: warehouseDetails,
            warehouse_conditions: warehouseConditions,
            distributor_media_path: distributorMediaPath,
            quality_check_results: qualityCheckResults,
            certifications_at_checkpoint: certificationsAtCheckpoint,
            testing_methods_used: testingMethodsUsed,
            corrective_actions: correctiveActions,
            checkpoint_media_path: checkpointMediaPath,
            timestamp: timestamp
        };

        // Send data to the server using fetch API
        fetch('/update_database', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response from the server (e.g., show a success message)
            console.log('Data saved successfully:', data);
        })
        .catch(error => {
            // Handle errors
            console.error('Error saving data:', error);
        });
    }
</script>
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

@app.route('/update_database', methods=['POST'])
def update_database():
    # Get data from the request
    data = request.json

    # Your database credentials
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='chainharbor'
    )

    try:
        # Update the database with the received data
        with db_connection.cursor() as cursor:
            query = """
            UPDATE batches SET
                receipt_datetime = %s,
                transportation_details = %s,
                storage_conditions = %s,
                received_quantity = %s,
                incidents_and_deviations = %s,
                handling_procedures = %s,
                warehouse_details = %s,
                warehouse_conditions = %s,
                distributor_media_path = %s,
                quality_check_results = %s,
                certifications_at_checkpoint = %s,
                testing_methods_used = %s,
                corrective_actions = %s,
                checkpoint_media_path = %s,
                timestamp = %s
            WHERE batch_id = %s
            """
            cursor.execute(query, (
                data['receipt_datetime'],
                data['transportation_details'],
                data['storage_conditions'],
                data['received_quantity'],
                data['incidents_and_deviations'],
                data['handling_procedures'],
                data['warehouse_details'],
                data['warehouse_conditions'],
                data['distributor_media_path'],
                data['quality_check_results'],
                data['certifications_at_checkpoint'],
                data['testing_methods_used'],
                data['corrective_actions'],
                data['checkpoint_media_path'],
                data['timestamp'],
                data['batch_id']
            ))

            db_connection.commit()

            return jsonify({'success': True, 'message': 'Data updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if db_connection.is_connected():
            db_connection.close()

if __name__ == "__main__":
    scan_qr_code()


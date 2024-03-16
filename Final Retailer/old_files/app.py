from flask import Flask, render_template, request
import cv2
from pyzbar.pyzbar import decode
import csv

app = Flask(__name__)

data = {}

def check_pid_exists(pid):
    with open('pid_wallet_mapping.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == pid:
                return row[1]  # Return the existing Wallet Address
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_qr_code():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame")
            break

        decoded_objects = decode(frame)

        cv2.imshow('QR Code Scanner', frame)

        for obj in decoded_objects:
            pid = obj.data.decode('utf-8')
            print(f"QR Code Data: {pid}")

            existing_wallet_address = check_pid_exists(pid)

            if existing_wallet_address:
                print("Error: PID {} is already mapped to Wallet Address {}".format(pid, existing_wallet_address))
                cap.release()
                cv2.destroyAllWindows()
                return render_template('index.html', error="PID already mapped")

            return render_template('enter_wallet_address.html', pid=pid)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

@app.route('/submit_wallet_address', methods=['POST'])
def submit_wallet_address():
    pid = request.form['pid']
    wallet_address = request.form['wallet_address']

    with open('pid_wallet_mapping.csv', 'a', newline='') as csvfile:
        fieldnames = ['PID', 'Wallet_Address']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'PID': pid, 'Wallet_Address': wallet_address})

    return render_template('index.html', error="Mapping successful")

if __name__ == '__main__':
    app.run(debug=True)

import cv2
from pyzbar.pyzbar import decode
from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

def scan_qr_code():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        decoded_objects = decode(frame)

        cv2.imshow('QR Code Scanner', frame)

        for obj in decoded_objects:
            data = obj.data.decode('utf-8')
            print(f"{data}")
            cap.release()
            cv2.destroyAllWindows()
            return data

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scan_qr', methods=['POST'])
def scan_qr():
    scanned_data = scan_qr_code()
    session['scanned_data'] = scanned_data
    return redirect(url_for('index'))

@app.route('/index')
def index():
    scanned_data = session.get('scanned_data', None)
    return render_template('index.html', scanned_data=scanned_data)

if __name__ == '__main__':
    app.run(debug=True , port=8000)

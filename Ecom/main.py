from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    product_details = {
        'name': 'Protinex Health And Nutritional Protein Drink Mix For Adults',
        'price': 604,
        'image_url': 'https://m.media-amazon.com/images/I/81bOrxfKi-L._SX679_.jpg'
    }
    return render_template('index.html', product=product_details)

@app.route('/buy_now', methods=['GET', 'POST'])
def buy_now():
    if request.method == 'POST':
        house_address = request.form.get('house_address')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open('orders.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([house_address, timestamp, 604])
        
        return f"Order placed successfully! {timestamp}"

    return render_template('buy_now.html')

@app.route('/sustainable_order', methods=['GET', 'POST'])
def sustainable_order():
    if request.method == 'POST':
        house_address = request.form.get('house_address')
        wallet_address = request.form.get('wallet_address')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        original_price = 604
        updated_price = original_price * 0.95
        
        with open('orders.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([house_address, timestamp, updated_price, wallet_address])
        
        return f"Sustainable order placed successfully! {timestamp}"

    return render_template('sustainable_order.html')

@app.route('/retailer_orders')
def retailer_orders():
    orders = []
    with open('orders.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            orders.append({
                'House Address': row[0],
                'Timestamp': row[1],
                'Price': row[2] if len(row) == 3 else row[2],
                'Wallet Address': row[3] if len(row) == 4 else ''
            })

    return render_template('retailer_orders.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True, port=1024)

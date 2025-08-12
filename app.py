from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root", 
    password="2301",  
    database="LaundryManagement"
)
cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
   
    cursor.execute("SELECT id, service_name FROM ServiceType")
    service_types = cursor.fetchall()
    
   
    print(service_types)  

    if request.method == 'POST':
       
        customer_name = request.form['customer_name']
        service_type_id = request.form['service_type_id']
        amount = request.form['amount']
        date_received = request.form['date_received']
        priority = request.form['priority']
        num_shirts = request.form['num_shirts']
        num_pants = request.form['num_pants']
        num_other = request.form['num_other']

    
        cursor.execute("INSERT INTO NewLaundry (customer_name, service_type_id, date_received, priority, amount, num_shirts, num_pants, num_other) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (customer_name, service_type_id, date_received, priority, amount, num_shirts, num_pants, num_other))
        db.commit()
        return redirect('/records')

    return render_template('index.html', service_types=service_types)

@app.route('/records')
def records():
    cursor.execute("SELECT id, customer_name, service_type_id, date_received, priority, amount, num_shirts, num_pants, num_other FROM NewLaundry")
    records = cursor.fetchall()

    
    for record in records:
        cursor.execute("SELECT service_name FROM ServiceType WHERE id = %s", (record[2],))
        service_type = cursor.fetchone()
        record += (service_type[0],) 

    return render_template('records.html', records=records)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    cursor.execute("DELETE FROM NewLaundry WHERE id = %s", (id,))
    db.commit()
    return redirect('/records')

@app.route('/clear', methods=['POST'])
def clear_records():
    cursor.execute("DELETE FROM NewLaundry")
    db.commit()
    return redirect('/records')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template

app = Flask(__name__)

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return 'Error: Division by zero'
    return a / b

def watt_to_dbm(watt):
    import math
    dbm = 10 * math.log10(watt * 1000)
    return dbm

def dBm_to_watt(dBm):
    import math
    watt = 10 ** (dBm / 10) / 1000
    return watt

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    operation = request.form['operation']
    num1 = float(request.form['num1'])
    num2 = float(request.form['num2'])
    
    if operation == 'add':
        result = add(num1, num2)
    elif operation == 'subtract':
        result = subtract(num1, num2)
    elif operation == 'multiply':
        result = multiply(num1, num2)
    elif operation == 'divide':
        result = divide(num1, num2)
    else:
        result = 'Invalid operation'
    
    return render_template('home.html', result=result)


@app.route('/conversion', methods=['POST'])
def conversion():
    power = float(request.form['power'])
    operation = request.form['operation1']
    if operation == 'dBm':
        powerAfterConversion = watt_to_dbm(power)
    else:
        powerAfterConversion = dBm_to_watt(power)
    return render_template('home.html', dBm=powerAfterConversion, selected_operation=operation, input_power=power)


if __name__ == '__main__':
    app.run(debug=True)

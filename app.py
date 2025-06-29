from flask import Flask, request, render_template
from pdf_search_logic import search_content  # Assuming pdf_search_logic.py contains the search logic for PDFs
from gpt2_connector import  GPT2Connector
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
import asyncio
import math

app = Flask(__name__)
gpt2_service = GPT2Connector()

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
    dbm = 10 * math.log10(watt * 1000)
    return dbm

def dBm_to_watt(dBm):
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

@app.route('/search', methods=['POST'])
def search():
    content = str(request.form['query'])
    output = search_content(content)
   
    # Build prompt for GPT-2
    prompt = f"Based on the following document excerpt:\n\n{output}\n\nAnswer this question:\n{content}"
    
   # Run GPT-2 asynchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(gpt2_service.get_chat_message_contents(messages=prompt,settings=PromptExecutionSettings()))
    
    gpt2_answer = (response[0].content)
    return render_template('home.html', searching=gpt2_answer, search=content)

    #if not result:
       # content = 'No results found.'
   # else:
      #  content = f'Search results for "{content}": {result}'
    #return render_template('home.html', searching=output, search=content)


if __name__ == '__main__':
    app.run(debug=True)

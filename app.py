import uuid
from lxml import etree as ET
from io import BytesIO
from flask import Flask, render_template, request

from lpb_bank.gateway import PaymentGateway

app = Flask(__name__)
global_data = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/payment/create/')
def payment_create():
    gateway = PaymentGateway()
    gateway.callback = 'http://127.0.0.1:5000/payment/success/'
    gateway.error_callback = 'http://127.0.0.1:5000/payment/fail/'
    data = {
        "AutoDeposit": True,
        "Payment": {
            "Mode": "3",                   # Unsigned short (3 or 5)
            "Descriptor": "QWERTY",
        },
        "Order": {
            "ID": str(uuid.uuid4()),
            "Amount": int(10 * 100),   # сумма в копейках
            "Currency": "EUR",
            "Description": "Пополнение баланса",
        },
        "Notification": "I agree with terms and conitions",
    }
    xml_data = gateway.prepare_data(data)
    pretty_xml_data = ET.tostring(ET.parse(
        BytesIO(xml_data)), 
        pretty_print=True, 
        encoding='utf-8', 
        xml_declaration=True, 
        standalone='yes'
    ).decode()
    form_fields = gateway.setup_purchase(xml_data=xml_data)
    form_action = gateway.config.url
    return render_template(
            'payment_form.html', 
            context=data, 
            form_action=form_action,
            form_fields=form_fields,
            xml_data=pretty_xml_data)


@app.route('/payment/success/', methods=['POST', 'GET'])
def payment_success():
    data = None
    if request.method == 'POST':
        data = request.form
        gateway = PaymentGateway()
        response_xml_data = gateway.parse_response(data).decode()
    return render_template(
        'payment_success.html', 
        form_action='#',
        form_fields=data,
        xml_data=response_xml_data)


@app.route('/payment/fail/', methods=['POST', 'GET'])
def payment_fail():
    data = None
    if request.method == 'POST':
        data = request.form
    return render_template(
        'payment_fail.html', 
        form_action='#',
        form_fields=data)


@app.route('/token/create/')
def token_create():
    global global_data
    gateway = PaymentGateway(payment_mode=5)
    gateway.callback = 'http://127.0.0.1:5000/token/success/'
    gateway.error_callback = 'http://127.0.0.1:5000/token/fail/'
    global_data['token'] = str(uuid.uuid4())
    data = {
        'Card': {
            'Token': global_data.get('token'),
        }
    }
    xml_data = gateway.prepare_data(data)
    pretty_xml_data = ET.tostring(ET.parse(
        BytesIO(xml_data)), 
        pretty_print=True, 
        encoding='utf-8', 
        xml_declaration=True, 
        standalone='yes'
    )
    form_fields = gateway.setup_purchase(xml_data=xml_data)
    form_action = gateway.config.token_url

    return render_template(
            'token_form.html', 
            context=data, 
            form_action=form_action,
            form_fields=form_fields,
            xml_data=pretty_xml_data.decode())


@app.route('/token/success/', methods=['POST', 'GET'])
def token_success():
    data = None
    if request.method == 'POST':
        data = request.form
        gateway = PaymentGateway()
        response_xml_data = gateway.parse_response(data).decode()
    return render_template(
        'token_success.html', 
        token=global_data.get('token'), 
        form_action='#',
        form_fields=data,
        xml_data=response_xml_data)


@app.route('/token/fail/', methods=['POST', 'GET'])
def token_fail():
    data = None
    if request.method == 'POST':
        data = request.form
    return render_template(
        'token_fail.html', 
        form_action='#',
        form_fields=data)


if __name__ == "__main__":
    app.run(debug=True)

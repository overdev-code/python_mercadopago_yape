from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import mercadopago
import uuid
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

load_dotenv("/.env")

def generate_idempotency_key():
    return str(uuid.uuid4())

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/pagar-con-yape', methods=['POST'])
def pagar_con_yape():
    token = request.form.get("token")
    description = request.form.get("description")
    payer_email  = request.form.get("payer_email")
    transaction_amount = 5 # aqui debes poner el monto que vas a cobrar
    access_token = os.getenv("ACCESS_TOKEN")
    if token:
        # Configura tu Access Token
        sdk = mercadopago.SDK(access_token)
        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {
            'x-idempotency-key': generate_idempotency_key(), # debe ser unico por pago 
        }

        payment_data = {
            "description": description,
            "installments": 1,
            "payer": {
                "email": payer_email,
            },
            "payment_method_id": "yape",
            "token": token,
            "transaction_amount": float(transaction_amount),
        }

        payment_response = sdk.payment().create(payment_data, request_options)
        payment = payment_response["response"]

        return payment

if __name__ == '__main__':
    app.run(debug=True)

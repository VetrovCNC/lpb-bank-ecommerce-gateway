import base64
from lxml import etree as ET
from suds.client import Client
from suds import WebFault
from Crypto.Cipher import ARC4
from Crypto.Cipher import PKCS1_v1_5 
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_v1_5_sign
from Crypto.Hash import SHA
from Crypto.Random import get_random_bytes
from io import BytesIO
import logging

from .config import GatewayConfig


log = logging.getLogger(__name__)


class PaymentGateway:
    """LPB Bank E-commerce Gateway"""

    def __init__(self):
        self.config = GatewayConfig()
        self.gateway_key = RSA.importKey(self.config.gateway_key)
        self.merchant_key = RSA.importKey(self.config.merchant_key)

    def setup_purchase(self, xml_data, form_request=True):
        encrypted_data = self.encrypt_data(xml_data)
        resp_data = {
            "INTERFACE": self.config.interface_code,
            "KEY_INDEX": self.config.key_index,
            "KEY": encrypted_data["key"],
            "DATA": encrypted_data["data"],
            "SIGNATURE": self.generate_signature(xml_data),
        }
        if form_request:
            resp_data.update(
                CALLBACK=self.config.callback,
                ERROR_CALLBACK=self.config.error_callback,
            )
        return resp_data

    def parse_response(self, response):
        data = self.decrypt_data(
            base64.b64decode(response["DATA"]), 
            base64.b64decode(response["KEY"]),
        )
        if not self.check_signature(data, base64.b64decode(response["SIGNATURE"])):
            return None
        root = ET.parse(BytesIO(data)).getroot()
        return ET.tostring(root, 
                           pretty_print=True, 
                           encoding="utf-8", 
                           xml_declaration=True, 
                           standalone="yes")

    def prepare_data(self, data):

        def create_elements(parent, data_dict):
            for key, value in data_dict.items():
                if value and isinstance(value, dict):
                    next_parent = ET.SubElement(parent, key)
                    create_elements(next_parent, value)
                elif value or isinstance(value, bool):
                    element = ET.SubElement(parent, key)
                    if isinstance(value, bool):
                        element.text = str(value).lower()
                    elif isinstance(value, int):
                        element.text = str(value)
                    else:
                        element.text = value
        root = ET.Element("data")
        create_elements(root, data)
        return ET.tostring(root, encoding="utf-8", xml_declaration=True, standalone="yes")

    def encrypt_data(self, data):
        # Генерация RC4 ключа
        rc4_key = get_random_bytes(16)
        # Шифрование данных с помощью RC4
        cipher = ARC4.new(rc4_key)
        encrypted_data = cipher.encrypt(data)
        # Кодирование зашифрованных данных в Base64
        b64_encrypted_data = base64.b64encode(encrypted_data)
        # Зашифрование RC4 ключа с помощью RSA и PKCS1_v1_5
        cipher_rsa = PKCS1_v1_5.new(self.gateway_key)
        encrypted_rc4_key = cipher_rsa.encrypt(rc4_key)
        # Кодирование зашифрованного RC4 ключа в Base64
        b64_encrypted_rc4_key = base64.b64encode(encrypted_rc4_key)
        return {
            "data": b64_encrypted_data.decode(),
            "key":  b64_encrypted_rc4_key.decode(),
        }

    def decrypt_data(self, data, key):
        sentinel = get_random_bytes(16)
        cipher_rsa = PKCS1_v1_5.new(self.merchant_key)
        key = cipher_rsa.decrypt(key, sentinel)
        cipher = ARC4.new(key)
        return cipher.decrypt(data)

    def generate_signature(self, data):
        h = SHA.new(data)
        signature = PKCS1_v1_5_sign.new(self.merchant_key).sign(h)
        return base64.b64encode(signature).decode()

    def check_signature(self, data, signature):
        h = SHA.new(data)
        verifier = PKCS1_v1_5_sign.new(self.gateway_key)
        return verifier.verify(h, signature)


class PaymentGatewaySOAP:
    """LPB Bank E-commerce Gateway SOAP"""

    def __init__(self, gateway: PaymentGateway):
        self._gateway = gateway
        self._soap = Client(url=self._gateway.config.soap_url)

    def _setup_purchase(self, data):
        xml_data = self._gateway.prepare_data(data)
        form_fields = self._gateway.setup_purchase(xml_data=xml_data, form_request=False)
        return form_fields

    def request(self, method, data):
        form_fields = self._setup_purchase(data)
        try:
            response = method(**form_fields)
            response_xml_data = self._gateway.parse_response(response)
        except WebFault as e:
            log.error(f"SOAP EXCEPTION: {e.fault.faultcode} - {e.fault.faultstring}")
            return {"status": "error", 
                    "faultcode": e.fault.faultcode, 
                    "faultstring": e.fault.faultstring}
        return {"status": "success", 
                "xml_data": response_xml_data}

    def authenticate(self, data):
        response = self.request(self._soap.service.Authenticate, data)
        return response
    
    def deposit(self, data):
        response = self.request(self._soap.service.Deposit, data)
        return response
    
    def get_payment(self, data):
        response = self.request(self._soap.service.GetPayment, data)
        return response

    def payment(self, data):
        response = self.request(self._soap.service.Payment, data)
        return response

    def register_token(self, data):
        response = self.request(self._soap.service.RegisterToken, data)
        return response
    
    def reverse(self, data):
        response = self.request(self._soap.service.Reverse, data)
        return response

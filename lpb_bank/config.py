import io
import os
from .settings import (
    ERROR_URL,
    GATEWAY_KEY,
    INTERFACE_CODE,
    KEY_INDEX,
    MERCHANT_KEY,
    PRODUCTION_BASE_URL,
    SANDBOX_MODE,
    DEMO_BASE_URL,
    PAYMENT_PATH,
    SUCCESS_URL,
    TOKEN_PATH,
    WSDL_SOAP_PATH,
)


class GatewayConfig:
 
    merchant_key = None

    def __init__(self, *args, **kwargs):
        if SANDBOX_MODE:
            self.url = DEMO_BASE_URL + PAYMENT_PATH
            self.token_url = DEMO_BASE_URL + TOKEN_PATH
            self.soap_url = DEMO_BASE_URL + WSDL_SOAP_PATH
        else:
            self.url = PRODUCTION_BASE_URL + PAYMENT_PATH
            self.token_url = PRODUCTION_BASE_URL + TOKEN_PATH
            self.soap_url = PRODUCTION_BASE_URL + WSDL_SOAP_PATH

        # Your merchant ID from Medoro account
        self.interface_code = INTERFACE_CODE

        # Key Index from ENCRYPTION KEYS table on your Medoro account
        self.key_index = KEY_INDEX

        # Content of gateway public key file that you need to download from  ENCRYPTION KEYS table on your Medoro account
        if isinstance(GATEWAY_KEY, io.IOBase):
            self.gateway_key = GATEWAY_KEY.read()
            GATEWAY_KEY.close()
        elif os.path.isfile(GATEWAY_KEY):
            with open(GATEWAY_KEY, 'r') as f:
                self.gateway_key = f.read()
        else:
            self.gateway_key = GATEWAY_KEY

        # Content of your private key that was generated
        if isinstance(MERCHANT_KEY, io.IOBase):
            self.merchant_key = MERCHANT_KEY.read()
            MERCHANT_KEY.close()
        elif os.path.isfile(MERCHANT_KEY):
            with open(MERCHANT_KEY, 'r') as f:
                self.merchant_key = f.read()
        else:
            self.merchant_key = MERCHANT_KEY

        self.callback = SUCCESS_URL
        self.error_callback = ERROR_URL

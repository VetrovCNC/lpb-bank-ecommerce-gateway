import os

BASE_DIR = os.path.dirname(__file__)

# =========================================
# LPB Bank E-commerce Gateway configuration
#==========================================

PRODUCTION_BASE_URL = 'https://ipsp.lv'
DEMO_BASE_URL = 'https://demo.ipsp.lv'

PAYMENT_PATH = '/form/v2/'
TOKEN_PATH = '/form/v2/token/'
WSDL_SOAP_PATH = '/api/v2/soap?wsdl'

SANDBOX_MODE = True

# MID (Interface Code). It was given to you by the manager when registering in the
# Medoro system.
INTERFACE_CODE = 3799525

# Key Index. After you upload the public key issued to you into the Medoro system,
# the key will appear in the list under the number assigned to it.
KEY_INDEX = 3

# "Medoro" Gateway Key. Upload the public part of the merchant key to the merchant
# interface (ipsp.lv → Merchants → your mid → Keys). Then download the public
# part of the Bank key ( Gateway Key ) from the same system.

#GATEWAY_KEY =  os.path.join(BASE_DIR, 'keys', 'gatewayKey.pem')

GATEWAY_KEY =  """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuwzKQu+W0QQ0Gp44jEay
FXBqOU6PvEVb7dKVsCFfJag2ISlbTFBLiHSgU5MJhyXJrCcmVmmH3fMZ9iJ95LhR
rM7VsvUIUHWHQiJ2I+gQbxIg94VOUcjvn6veIpYbxxRGy0BvcVv+6jTyzTZMGrx+
EoNKcJB3zqqkJy+PN7vKkTdyF7r+6WWsPDtAbgcg95d+FahxIEycFZOsDYPVJrow
nDAlEt8pUgL7AhLc52rUbVTkcCYuZqAQBVVRQUoAXpe1+CTn9oDVnEz0JluOTyHn
Cc8DDv90qsFP+cH2LcAF+YvZWrHME7XtzFYM1YddMIOaMBrk4t0X16To8b2Sz4wl
ywIDAQAB
-----END PUBLIC KEY-----

"""

# Merchant Key. It is generated by your IT manager using OpenSSL.
MERCHANT_KEY = os.path.join(BASE_DIR, 'keys', 'privkey.pem')

# Покупатель попадает на эту страницу в случае успешной оплаты
SUCCESS_URL = 'http://127.0.0.1:5000/payment/success/'

#  Покупатель попадает на эту страницу в случае возникновения ошибки при оплате
ERROR_URL = 'http://127.0.0.1:5000/payment/fail/'

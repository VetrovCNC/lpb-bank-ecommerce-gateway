import uuid
import logging
from lpb_bank.gateway import PaymentGateway, PaymentGatewaySOAP

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


gateway = PaymentGateway()
soap = PaymentGatewaySOAP(gateway)


def test_authenticate(d3d_acs_pares, payment_id=None, order_id=None):
    log.debug("SOAP: Authenticate request")
    if payment_id is not None:
        data = {
            "Payment": {
                "ID": payment_id,
            },
        }
    elif order_id is not None:
        data = {
            "Order": {
                "ID": order_id,
            },
        }
    data.update(D3D=dict(PaRes=d3d_acs_pares))

    resp = soap.authenticate(data)
    if resp.get("status") == "success":
        xml_data = resp.get("xml_data").decode()
        log.debug(xml_data)
    return resp
    

def test_deposit(deposit_amount: float, payment_id=None, order_id=None):
    log.debug('SOAP: Deposit request')
    if payment_id is not None:
        data = {
            "Payment": {
                "ID": payment_id,
            },
            "Order": {
                "DepositAmount": int(deposit_amount * 100),   # сумма в копейках
            },
        }
    elif order_id is not None:
        data = {
            "Order": {
                "ID": order_id,
                "DepositAmount": int(deposit_amount * 100),   # сумма в копейках
            },
        }
    resp = soap.deposit(data)
    if resp.get("status") == "success":
        xml_data = resp.get("xml_data").decode()
        log.debug(xml_data)
    return resp


def test_get_payment(payment_id=None, order_id=None):
    log.debug('SOAP: GetPayment request')
    if payment_id is not None:
        data = {
            "Payment": {
                "ID": payment_id,
            },
        }
    elif order_id is not None:
        data = {
            "Order": {
                "ID": order_id,
            },
        }
    resp = soap.get_payment(data)
    if resp.get("status") == "success":
        xml_data = resp.get("xml_data").decode()
        log.debug(xml_data)
    return resp


def test_payment():
    log.debug('SOAP: Payment request')
    data = {
        "AutoDeposit": True,
        "Payment": {
            "Mode": "4",     # 4 or 6
        },
        "Order": {
            "ID": str(uuid.uuid4()),
            "Amount": int(10 * 100),
            "Currency": "EUR",
            "Description": "Пополнение баланса",
        },
        "Card": {
            "Number": "5444870724493746",   # 13-19 digit number
            "Name": "test",                 # Under 50 utf8 chars
            "Expiry": "2304",               # First year, then month
            "CSC": "999"                    # Exactly 3 digits
        },
        "RemoteAddress": "78.26.151.11",    # This MUST be cardholders IP
    }
    resp = soap.payment(data)
    if resp.get("status") == "success":
        xml_data = resp.get("xml_data").decode()
        log.debug(xml_data)
    return resp


def test_register_token(token, name, number, expiry):
    log.debug('SOAP: RegisterToken request')
    data = {
        "Card": {
            "Token": str(token),
            "Name": name,            # Under 50 utf8 chars
            "Number": str(number),   # 13-19 digit number
            "Expiry": str(expiry),   # First year, then month
        },
    }
    resp = soap.register_token(data)
    if resp.get("status") == "success":
        xml_data = resp.get("xml_data").decode()
        log.debug(xml_data)
    return resp


def test_reverse(reversal_amount: float, payment_id=None, order_id=None):
    log.debug('SOAP: Reverse request')
    if payment_id is not None:
        data = {
            "Payment": {
                "ID": payment_id,
            },
            "Order": {
                "ReversalAmount": int(reversal_amount * 100),
            },
        }
    elif order_id is not None:
        data = {
            "Order": {
                "ID": order_id,
                "ReversalAmount": int(reversal_amount * 100),
            },
        }
    resp = soap.reverse(data)
    if resp.get("status") == "success":
        xml_data = resp.get("xml_data").decode()
        log.debug(xml_data)
    return resp


if __name__ == "__main__":
    log.debug('Тестируем SOAP интерфейс')

    # test_payment()

    # test_deposit(10, payment_id=180863533)

    # test_reverse(3.0, payment_id=180863531)

    # test_authenticate("PaRes", order_id=str(uuid.uuid4()))

    # test_get_payment(payment_id=180863299)

    # test_register_token(
    #     token=uuid.uuid4(),
    #     name="Test", 
    #     number=5444870724493746, 
    #     expiry=2304,
    # )

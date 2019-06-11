from DAL.ApiController import getPINResponse
from DAL.ApiController import getToken
from BLL.CustomErrors import *
from BLL.Logic import writejson

def test():

    cardId = 'cB7K+6hwm+dCBmoNT76N7CPONRFTepfWql3jQ7n9+g=0000'
    token = getToken()
    amount = 50.00
    pin = '5909'
    response = getPINResponse(token, amount, pin, cardId)
    while not response.status_code == 201:
        if response.status_code == 401:
            if response.text == 'Unauthorized':
                token = getToken()
                response = getPINResponse(token, amount, pin, cardId)
                print('wrong token')
            else:
                print('Incorrect PIN.')
                pin = '5900'
                response = getPINResponse(token, amount, pin, cardId)
        elif response.status_code == 404:
            print('Kaart is niet herkend. Probeer opnieuw.')
            cardId = 'cB7K+6hwm+dZCBmoNT76N7CPONRFTepfWql3jQ7n9+g=0000'
            pin = '5900'
            response = getPINResponse(token, amount, pin, cardId)
        elif response.status_code == 429 or response.status_code == 403:
            raise UserError('Kaart is geblokkeerd.')
        elif response.status_code == 400:
            raise UserError('Onvoldoende Saldo.')
        elif response.status_code == 403:
            raise UserError('Toegang geweigerd.')
        else:
            raise CancelError
    print('TOT {0} EUR'.format(amount))
    print('AKKOORD')


try:
    test()
except UserError as e:
    print(str(e))
except CancelError:
    print("cancelled")
except ApiError as e:
    print(str(e))



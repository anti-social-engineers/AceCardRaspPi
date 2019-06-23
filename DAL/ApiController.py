import json
import requests
from BLL.CustomErrors import ApiError

"""
Request a token from the API for the payment functionality
"""

def getTokenResponse():
    url = 'https://api.aceofclubs.nl/api/login'
    data = openConfig()
    params = {
        "email" : data['email'],
        "password" : data['password']
    }
    return requests.post(url, json = params)

def getToken():
    reponse = getTokenResponse()
    if reponse.status_code == 500:
        raise ApiError('Error token 500')
    return reponse.json()['jsonWebToken']

def openConfig():
    with open('config.json') as json_file:
        return json.load(json_file)

"""
Send a POST request to the API for the payment transaction
We handle the reponse in the front-end by displaying for example if the PIN is wrong.
"""
def getPaymentResponse(token, amount, cardPin, cardId):
    headers = {'Authorization': 'Bearer {0}'.format(token)}
    url = "{0}{1}".format(openConfig()['BaseURL'], 'club/payment')
    print(amount, cardPin, cardId)
    params = {
        "club_id" : openConfig()['ClubId'],
        "card_code" : cardId,
        "card_pin" : cardPin,
        "amount" : amount
    }
    return requests.post(url, json=params, headers=headers)


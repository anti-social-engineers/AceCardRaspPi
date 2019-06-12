import json
import requests
from BLL.CustomErrors import ApiError

def getTokenResponse():
    url = 'https://api.aceofclubs.nl/api/login'
    data = openConfig()
    params = {
        "email" : data['email'],
        "password" : data['password']
    }
    return requests.post(url, json = params)

def openConfig():
    with open('config.json') as json_file:
        return json.load(json_file)

def getToken():
    reponse = getTokenResponse()
    if reponse.status_code == 500:
        raise ApiError('Error 500')
    return reponse.json()['jsonWebToken']

def getPINResponse(token, amount, cardPin, cardId):
    headers = {'Authorization': 'Bearer {0}'.format(token)}
    url = 'https://api.aceofclubs.nl/api/club/payment'
    print(amount, cardPin, cardId)
    params = {
        "club_id" : getClubId(),
        "card_code" : cardId,
        "card_pin" : cardPin,
        "amount" : amount
    }
    return requests.post(url, json=params, headers=headers)

def getCardKey():
    return openConfig()['CardKey']

def getClubId():
    return openConfig()['ClubId']
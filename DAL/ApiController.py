import json
import requests

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
    return reponse.json()['jsonWebToken']

def getPINResponse(pincode, cardId, amount):
    token = getToken()
    headers = {'Authorization': token}
    url = 'https://api.aceofclubs.nl/'
    params = {
        "cardid" : cardId,
        "pincode" : pincode,
        "amount" : amount
    }
    return requests.get(url, params, headers=headers)


def getCardKey():
    return openConfig()['CardKey']
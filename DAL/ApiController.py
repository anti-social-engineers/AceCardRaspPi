import json
import requests

def getTokenResponse():
    url = 'https://api.aceofclubs.nl/api/login'
    data = openConfig()
    params = {
        "email" : data['email'],
        "password" : data['password']
    }
    print(params)
    return requests.post(url, json = params)

def openConfig():
    with open('config.json') as json_file:
        return json.load(json_file)

def getToken():
    reponse = getTokenResponse()
    return reponse.json()['jsonWebToken']

def getPINResponse(pincode, cardId, token):
    token = getToken()
    url = 'https://api.aceofclubs.nl/'
    params = {
        "cardid" : cardId,
        "pincode" : pincode
    }
    reponse = requests.get(url, params)
    if reponse.status_code == 400:
        return Exception("Pin Incorrect")
    elif reponse.status_code == 500:
        return Exception("No Saldo")
    else:
        return True


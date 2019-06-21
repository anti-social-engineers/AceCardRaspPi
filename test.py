import json

def writejson():
    data = {'email': 'owner@aceofclubs.nl', 'password': 'helloworld123',
            'Encryptionkey': 'C*F-JaNdRgUjXn2r5u8x/A?D(G+KbPeS', 'BaseURL' : 'https://api.aceofclubs.nl/api/', 'ClubId' : '2d466140-f70b-4ac3-8156-ee922657bacd'}
    with open('config.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

writejson()
import json

def writejson():
    data = {'email': 'owner@aceofclubs.nl', 'password': 'helloworld123',
            'Encryptionkey': 'C*F-JaNdRgUjXn2r5u8x/A?D(G+KbPeS', 'BaseURL' : 'https://api.aceofclubs.nl/api/', 'ClubId' : '1c7ef92f-5424-438f-84f4-ba0158ad06e4'}
    with open('config.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

writejson()
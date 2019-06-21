import json

def writejson():
    data = {'email': 'raspberry.pi@aceofclubs.nl', 'password': 'xpc^>smGBTRjKLs:Xk6&I>6&w5m~<WC-',
            'Encryptionkey': 'C*F-JaNdRgUjXn2r5u8x/A?D(G+KbPeS', 'CardKey' : [0x75, 0x42, 0x64, 0x35, 0x5f, 0x5d], 'ClubId' : '1c7ef92f-5424-438f-84f4-ba0158ad06e4'}
    with open('config.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

writejson()
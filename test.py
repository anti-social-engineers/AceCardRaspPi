from DAL.Encryption import AESecryption


test1 = 'qwerty12345query'

x = AESecryption()
print('{0} - {1}'.format(test1, x.encrypt(test1)))



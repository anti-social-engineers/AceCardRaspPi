import binascii
# a='1234567891234567891234567891234a'
# print(type(a))
# # s=binascii.unhexlify(a)
#
# b= bytearray(a, 'utf-16')
# print(type(b))
# t = len(b)
# print(t)
#
# value = format('hello')
#
#
# l = binascii.hexlify(b)
#
# print(l)


data = '123456789123456789A23C5678912345'
dataHex = binascii.unhexlify(data)
dataArray = bytearray(dataHex)
print(len(dataArray))
print(dataArray)

l = binascii.hexlify(dataArray)
print(l)

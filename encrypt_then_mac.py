
import binascii

from Crypto.Util import Counter
from Crypto.Cipher import AES
from os import urandom
from Crypto.Util.number import *

key = urandom(16)
iv = urandom(16)
mac_key = urandom(16)

blocksize = 16

def pad(input_str, blocksize):
	input_str += chr(blocksize - len(input_str) % blocksize)*(blocksize - len(input_str) % blocksize)
	assert len(input_str) % blocksize == 0
	return input_str

def unpad(input_str):
	#input_str[:-ord(input_str[-1])]
	return input_str[:-(input_str[-1])]

def cbc_mac_gen(input_str, iv, mac_key, blocksize):
	input_str=str(input_str)
	print(input_str)
	print("inputstr")
	input_str = pad(input_str, blocksize)
	print(input_str)
	print("inputstr2")
	input_str=bytes(input_str.encode())
	print(input_str)
	print("inputstr3")

	obj1 = AES.new(mac_key, AES.MODE_CBC, iv)
	auth_tag = obj1.encrypt(input_str)[-blocksize:]
	print(auth_tag)
	print("auth_tag")
	return auth_tag

def encrypt(input_str, iv, key, blocksize):
	input_str = pad(input_str, blocksize)
	print(input_str)
	print("input_str")

	obj1 = AES.new(key, AES.MODE_CBC, iv)
	ciphertext = obj1.encrypt((input_str.encode()))
	print(ciphertext)
	print("ciphertext")
	return ciphertext

def decrypt(ciphertext, iv, key, blocksize):
	obj1 = AES.new(key, AES.MODE_CBC, iv)
	plaintext = obj1.decrypt(ciphertext)
	print(plaintext)
	print("plaintext1")
	return unpad(plaintext)

def encrypt_then_mac(input_str, iv, key, mac_key, blocksize):
	ciphertext = encrypt(input_str, iv, key, blocksize)
	print(ciphertext)
	tag = cbc_mac_gen(ciphertext, iv, mac_key, blocksize)
	print(tag)
	print("tag")
	print(ciphertext)
	print("ciphertext")
	#return ciphertext.encode("hex") + ":" + tag.encode("hex")
	return ciphertext.hex() + ":" + tag.hex()

def auth_check(session_cookie, iv, key, mac_key, blocksize):
	ciphertext, tag = session_cookie.split(":")
	print(ciphertext)
	print("ciphertext")
	ciphertext = bytes.fromhex(ciphertext)
	print(ciphertext)
	print("ciphertext2")
	tag = bytes.fromhex(tag)
	print(tag)
	print("tag")
	if cbc_mac_gen(ciphertext, iv, mac_key, blocksize) == tag:
		print ("Authentication Successful")
		return decrypt(ciphertext, iv, key, blocksize)
	else:
		print ("Authentication Failed")
		return 0

str1 = encrypt_then_mac('testplaintext', iv, key, mac_key, 16)
print("STR11111111111111")
print(str1)

print (auth_check(str1, iv, key, mac_key, blocksize).decode())

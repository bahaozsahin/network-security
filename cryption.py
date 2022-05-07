
import binascii

from Crypto.Util import Counter
from Crypto.Cipher import AES
from os import urandom
from Crypto.Util.number import *
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
key = urandom(16)
iv = urandom(16)
mac_key = urandom(16)

blocksize = 16
##########################################################
public_key=""
private_key=""

def Asymmetric_Key_Generating():

	private_key = rsa.generate_private_key(
			public_exponent=65537,
			key_size=2048,
			backend=default_backend()
		)
	public_key = private_key.public_key()



	pem = private_key.private_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PrivateFormat.PKCS8,
			encryption_algorithm=serialization.NoEncryption()
		)
	with open('private_key.pem', 'wb') as f:
		f.write(pem)

	pem = public_key.public_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PublicFormat.SubjectPublicKeyInfo
		)
	with open('public_key.pem', 'wb') as f:
		f.write(pem)



def Asymmetric_Key_Reading():
	global private_key
	global public_key

	from cryptography.hazmat.backends import default_backend
	from cryptography.hazmat.primitives import serialization
	with open("private_key.pem", "rb") as key_file:
			private_key = serialization.load_pem_private_key(
				key_file.read(),
				password=None,
				backend=default_backend()
			)
	with open("public_key.pem", "rb") as key_file:
			public_key = serialization.load_pem_public_key(
				key_file.read(),
				backend=default_backend()
			)


# Encrypting and decrypting
def Asymmetric_Encrypt(message,public_key):


	#message = b'encrypt me!'
	encrypted = public_key.encrypt(
			message,
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA256()),
				algorithm=hashes.SHA256(),
				label=None
			)
		)
	return encrypted
def Asymmetric_Decrypt(encrypted,private_key):
	original_message = private_key.decrypt(
			encrypted,
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA256()),
				algorithm=hashes.SHA256(),
				label=None
			)
		)
	return original_message


##########################################################

def pad(input_str, blocksize):
	input_str += chr(blocksize - len(input_str) % blocksize)*(blocksize - len(input_str) % blocksize)
	assert len(input_str) % blocksize == 0
	return input_str

def unpad(input_str):
	#input_str[:-ord(input_str[-1])]
	return input_str[:-(input_str[-1])]

def cbc_mac_gen(input_str, iv, mac_key, blocksize):
	input_str=str(input_str)

	input_str = pad(input_str, blocksize)

	input_str=bytes(input_str.encode())


	obj1 = AES.new(mac_key, AES.MODE_CBC, iv)
	auth_tag = obj1.encrypt(input_str)[-blocksize:]

	return auth_tag

def encrypt(input_str, iv, key, blocksize):
	input_str = pad(input_str, blocksize)


	obj1 = AES.new(key, AES.MODE_CBC, iv)
	ciphertext = obj1.encrypt((input_str.encode()))

	return ciphertext

def decrypt(ciphertext, iv, key, blocksize):
	obj1 = AES.new(key, AES.MODE_CBC, iv)
	plaintext = obj1.decrypt(ciphertext)
	return unpad(plaintext)

def encrypt_then_mac(input_str, iv, key, mac_key, blocksize):
	ciphertext = encrypt(input_str, iv, key, blocksize)

	tag = cbc_mac_gen(ciphertext, iv, mac_key, blocksize)
	print("Giren ciphertext: " + str(ciphertext))
	print("Giren tag: " + str(tag))
	print("Giren iv: "+str(iv))

	print("Giren key: "+str(key))

	print("Giren mac_key: "+str(mac_key))

	print("Giren blocksize: "+str(blocksize))
	#return ciphertext.encode("hex") + ":" + tag.encode("hex")
	return ciphertext.hex() + ":" + tag.hex()

def auth_check(session_cookie, iv, key, mac_key, blocksize):
	ciphertext, tag = session_cookie.split(":")
	ciphertext = bytes.fromhex(ciphertext)
	tag = bytes.fromhex(tag)

	print("Çıkan ciphertext: " + str(ciphertext))
	print("Çıkan tag: " + str(tag))

	if cbc_mac_gen(ciphertext, iv, mac_key, blocksize) == tag:
		print ("Authentication Successful")
		return decrypt(ciphertext, iv, key, blocksize)
	else:
		print ("Authentication Failed")
		return 0

def combine_keys(auth,iv,key,mac_key,blocksize,public_key):
	combine_keys=iv.hex()+":"+key.hex()+":"+mac_key.hex()+":"+str(blocksize)
	combine_keys=combine_keys.encode()
	return Encrypt_Key(auth,combine_keys,public_key)

def separate_keys(auth,combine_keys):
	iv, key ,mac_key,blocksize= combine_keys.split(":")
	iv=bytes.fromhex(iv)
	key=bytes.fromhex(key)
	mac_key=bytes.fromhex(mac_key)
	blocksize=int(blocksize)

	print("Çıkan iv: "+str(iv))

	print("Çıkan key: "+str(key))

	print("Çıkan mac_key: "+str(mac_key))

	print("Çıkan blocksize: "+str(blocksize))
	return auth_check(auth, iv, key, mac_key, blocksize).decode()


def combine_File(auth,Encrypt_combine_keys):
	combine_file = auth + "::" + Encrypt_combine_keys.hex()
	print("Birleştirilen Dosya Sonuç: "+combine_file)
	return combine_file


def separate_File(combine_file):
	auth, Encrypt_combine_keys= combine_file.split("::")
	Encrypt_combine_keys=bytes.fromhex(Encrypt_combine_keys)
	combine_keys=Decrypt_Key(Encrypt_combine_keys,private_key)
	return separate_keys(auth,combine_keys)

def Encrypt_Key(auth,combine_keys,public_key):
	Encrypt_combine_keys=Asymmetric_Encrypt(combine_keys,public_key)
	return combine_File(auth,Encrypt_combine_keys)

def Decrypt_Key(Encrypt_combine_keys,private_key):
	Decrypt_Key = Asymmetric_Decrypt(Encrypt_combine_keys, private_key)
	Decrypt_Key=Decrypt_Key.decode()
	return Decrypt_Key

Asymmetric_Key_Reading()
auth = encrypt_then_mac('testplaintext', iv, key, mac_key, 16)
print("Auth:"+str(auth))
combine_File=combine_keys(auth,iv,key,mac_key,blocksize,public_key)


print("Sonuç:"+separate_File(combine_File))



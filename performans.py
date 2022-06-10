
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
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import errno

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

#import main

blocksize = 16
##########################################################
public_key=""
private_key=""
mymail=""

def SetMail(mail):
	global mymail
	mymail=mail

def Asymmetric_Key_Generating():
	new_key = RSA.generate(2048)

	private_key = new_key.exportKey("PEM")
	public_key = new_key.publickey().exportKey("PEM")

	fd = open("privateKey.key", "wb")
	fd.write(private_key)
	fd.close()

	fd = open("publicKey.key", "wb")
	fd.write(public_key)
	fd.close()



def Asymmetric_Key_Reading():
	global private_key
	global public_key

	private_key = RSA.import_key(open('privateKey.key').read())
	public_key = RSA.import_key(open('publicKey.key').read())

def Asymmetric_Sign(message,private_key):
	message = bytes(message.encode())
	hasher = SHA256.new(message)
	signer = PKCS1_v1_5.new(private_key)
	signature = signer.sign(hasher)
	return signature

def Asymmetric_Auth(message,signature,public_key):
	message=bytes(message.encode())
	hasher = SHA256.new(message)
	verifier = PKCS1_v1_5.new(public_key)
	if verifier.verify(hasher, signature):
		print('İmza Doğru')
		return 1
	else:
		print('İmza Yanlış ,Private Key yada Mesaj Değiştirilmiş')
		return 0

# Encrypting and decrypting
def Asymmetric_Encrypt(message,public_key):
	cipher = PKCS1_OAEP.new(public_key)
	encrypted = cipher.encrypt(message)
	return encrypted
def Asymmetric_Decrypt(encrypted,private_key):
	cipher = PKCS1_OAEP.new(private_key)
	#print(encrypted)
	encrypted=bytes(encrypted)
	original_message = cipher.decrypt(encrypted)
	return original_message


##########################################################



def cbc_mac_gen(input_str, iv, mac_key, blocksize):



	obj1 = AES.new(mac_key, AES.MODE_EAX, iv)
	auth_tag = obj1.encrypt(input_str)[-blocksize:]
	print("auth_tag")
	#print(auth_tag)
	return auth_tag

def encrypt(input_str, iv, key, blocksize):



	obj1 = AES.new(key, AES.MODE_EAX, iv)
	ciphertext = obj1.encrypt((input_str))

	return ciphertext

def decrypt(ciphertext, iv, key, blocksize):
	try:
		obj1 = AES.new(key, AES.MODE_EAX, iv)
		plaintext = obj1.decrypt(ciphertext)
		original_file= plaintext
		console="Dosya Başarıyla Çözüldü" + "\n"
		success=1

		return success,original_file,console
	except Exception as e:
		return 0, "", str(e) + "\n"

def encrypt_then_mac(path, iv, key, mac_key, blocksize):
	with open(path, "rb") as dosya:
		input_str=dosya.read()

	ciphertext = encrypt(input_str, iv, key, blocksize)

	tag = cbc_mac_gen(ciphertext, iv, mac_key, blocksize)
	#print("Giren ciphertext: " + str(ciphertext))
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

	#print("Çıkan ciphertext: " + str(ciphertext))
	print("Çıkan tag: " + str(tag))

	console=""

	if cbc_mac_gen(ciphertext, iv, mac_key, blocksize) == tag:
		print ("Authentication Başarılı")
		console+="Authentication Başarılı"+"\n"

		success,original_file,console2= decrypt(ciphertext, iv, key, blocksize)
		console+=console2
		return success, original_file, console


	else:
		print ("Authentication Başarısız")
		console += "Authentication Başarısız" + "\n"
		return 0, "", console


def combine_keys(maillist,auth,iv,key,mac_key,blocksize):

	combine_keys=iv.hex()+"::"+key.hex()+"::"+mac_key.hex()+"::"+str(blocksize)
	sign_combine_keys=Asymmetric_Sign(combine_keys,private_key).hex()
	print("sign: "+str(sign_combine_keys))
	#print("combine_keys: "+str(combine_keys))
	All=""
	combine_keys=combine_keys.encode()
	count=0
	for mailadress in maillist:
		kayitli=0
		if(mailadress==mymail):
			Encrypt_combine_keys = Asymmetric_Encrypt(combine_keys, public_key)
			person = bytes(mailadress.encode()).hex() + ":::" + Encrypt_combine_keys.hex()
			kayitli = 1
		else:
			try:
				person_public_key = RSA.import_key(open(mailadress+".pem").read())
				Encrypt_combine_keys = Asymmetric_Encrypt(combine_keys, person_public_key)
				person=bytes(mailadress.encode()).hex()+":::"+Encrypt_combine_keys.hex()
				kayitli = 1
			except:
				print(mailadress+" Kişi Kaydı Bulunamadı")
		if(kayitli==1):
			if(count!=0):
				All+="::::"+person
			else:
				All+=person
			count+=1
	print("All")
	#print(All)
	return combine_File(auth,All,sign_combine_keys)

def separate_keys(auth,combine_keys):
	iv, key ,mac_key,blocksize= combine_keys.split("::")
	iv=bytes.fromhex(iv)
	key=bytes.fromhex(key)
	mac_key=bytes.fromhex(mac_key)
	blocksize=int(blocksize)

	print("Çıkan iv: "+str(iv))

	print("Çıkan key: "+str(key))

	print("Çıkan mac_key: "+str(mac_key))

	print("Çıkan blocksize: "+str(blocksize))

	success,original_file,console=auth_check(auth, iv, key, mac_key, blocksize)



	return success,original_file,console


def combine_File(auth,All,sign_combine_keys):
	combine_file = auth + ":::::" + All+":::::"+sign_combine_keys+":::::"+bytes(mymail.encode()).hex()
	#print("Birleştirilen Dosya Sonuç: "+combine_file)
	return combine_file


def separate_File(combine_file):
	console=""
	auth, All,sign_combine_keys,sender= combine_file.split(":::::")
	persons=All.split("::::")
	sender=str(bytes.fromhex(sender).decode())
	sign_combine_keys = bytes.fromhex(sign_combine_keys)
	Encrypt_combine_keys=""



	for person in persons:

		person_mail,person_keys=person.split(":::")
		person_mail=str(bytes.fromhex(person_mail).decode())
		if(person_mail==mymail):
			Encrypt_combine_keys=person_keys


	#Mail Bulunursa
	if(Encrypt_combine_keys!=""):

		Encrypt_combine_keys=bytes.fromhex(Encrypt_combine_keys)
		#Gönderen Bizsek
		if(sender==mymail):
			combine_keys=Decrypt_Key(Encrypt_combine_keys,private_key)
			isSignTrue=Asymmetric_Auth(combine_keys,sign_combine_keys,public_key)
			if(isSignTrue==1):
				print("Gönderen Doğrulandı")
				console += "Gönderen Doğrulandı"+"\n"

				success, original_file, console2 = separate_keys(auth, combine_keys)
				console += console2
				return success, original_file, console

			else:
				print("Gönderen Doğrulanamadı İşlem İptal Edildi")
				console += "Gönderen Doğrulanamadı İşlem İptal Edildi" + "\n"
				return 0, "", console
		#Gönderen Başkası İse
		else:
			mail_valid=0
			try:
				person_public_key= RSA.import_key(open(sender+".pem").read())
				mail_valid = 1
			except:
				print("Bu Mail Adresine Ait Kayıt Bulunamadı İşlem İptal Edildi")
				console += "Bu Mail Adresine Ait Kayıt Bulunamadı İşlem İptal Edildi" + "\n"
				return 0, "", console
			if(mail_valid==1):
				try:
					combine_keys = Decrypt_Key(Encrypt_combine_keys, private_key)
					isSignTrue = Asymmetric_Auth(combine_keys, sign_combine_keys, person_public_key)
					if (isSignTrue == 1):
						print("Gönderen Doğrulandı")
						console += "Gönderen Doğrulandı" + "\n"

						success,original_file,console2=separate_keys(auth, combine_keys)
						console+=console2
						return success, original_file, console

					else:
						print("Gönderen Doğrulanamadı İşlemler İptal Edildi")
						console += "Gönderen Doğrulanamadı İşlemler İptal Edildi" + "\n"
						return 0, "", console
				except Exception as e:
					print(e)
					print("Dosya Değiştirilmiş İşlemler İptal Edildi")
					console += "Dosya Değiştirilmiş İşlemler İptal Edildi" + "\n"
					return 0, "", console

	else:
		print("Sizin Adınıza Key Bulunamadı İşlemler İptal Edildi")
		console += "Sizin Adınıza Key Bulunamadı İşlemler İptal Edildi" + "\n"
		return 0,"",console


def Decrypt_Key(Encrypt_combine_keys,private_key):
	Decrypt_Key = Asymmetric_Decrypt(Encrypt_combine_keys, private_key)
	Decrypt_Key=Decrypt_Key.decode()
	return Decrypt_Key


import time

class timer:
    def baslat(self):
        self.baslangic = time.perf_counter()

    def bitir(self):
        self.bitis = time.perf_counter()
        fark = (self.bitis-self.baslangic)*1000
        print(f"{fark} ms'de tamamlandı.")


if __name__ == '__main__':
	Asymmetric_Key_Generating()
	Asymmetric_Key_Reading()

	path = "C:/Users/pc/desktop/data_market.zip"
	path_download= "C:/Users/pc/desktop/data_market2.zip"

	#Simetrik ve Asimetrik karma
	#C:/Users/pc/desktop/Merged_document.pdf(3,05 MB) 55.331800000000044 ms'de tamamlandı.
	#C:/Users/pc/desktop/video1.mp4 (272 MB) 5809.743200000001 ms'de tamamlandı.
	#C:/Users/pc/desktop/data_market.zip (1,32 GB) 24875.9473 ms'de tamamlandı.


	#Asimetrik
	#Plain text uzunluğu Hatası veriyor

	#simetrik
	#C:/Users/pc/desktop/Merged_document.pdf(3,05 MB) 1.8352999999999842 ms'de tamamlandı.
	#C:/Users/pc/desktop/video1.mp4 (272 MB) 1592.5149999999999 ms'de tamamlandı.
	#C:/Users/pc/desktop/data_market.zip (1,32 GB)	8677.6264 ms'de tamamlandı.


	maillist=["mert_1998_61@hotmail.com"]
	SetMail("mert_1998_61@hotmail.com")

	timer = timer()
	timer.baslat()
	key = urandom(16)
	iv = urandom(16)
	mac_key = urandom(16)
	blocksize=16

	#simetrik
	#with open(path, "rb") as dosya:
	#	message=dosya.read()

	#encrypted=encrypt(message, iv,key,blocksize)

	#success,original_file,console=decrypt(encrypted, iv,key,blocksize)

	#f = open(path_download, "wb")
	#f.write(original_file)
	#f.close()





	auth = encrypt_then_mac(path, iv, key, mac_key, 16)
	#print("Auth:" + str(auth))
	combine_File = combine_keys(maillist,auth, iv, key, mac_key, blocksize)
	#print(original_file)
	#print(console)
	success, original_file, console=separate_File(combine_File)

	f = open(path_download, "wb")
	f.write(original_file)
	f.close()

	timer.bitir()

	#print(str(original_file.decode()))

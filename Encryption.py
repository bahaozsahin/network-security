def FunCrypt(orgFilePath):
    f = Fernet(key)
    orgFileName=os.path.basename(orgFilePath)
    encFileName="enc"+orgFileName
    decFileName = "dec" + orgFileName

    with open(orgFilePath, 'rb') as original_file:
        original = original_file.read()

    encrypted = f.encrypt(original)

    with open (encFilePath+encFileName, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
        print("Başarıyla Şifrelendi")

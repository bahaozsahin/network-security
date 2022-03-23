import dropbox

#auth token böyle verilmeyecek dışarıdan pushlanacak
authToken = "currentAuthToken"

#connect
dbx = dropbox.Dropbox(authToken)

def printAccInfo():
    print("---printing info about current account---")
    print(dbx.users_get_current_account())

def printDirectory():
    print("-----------------------Listing Files----------------------- ")
    for entry in dbx.files_list_folder('').entries:
        print(entry.name)

def printSpecifiedDirectory(path):
    files = dbx.files_list_folder(path).entries
    print("------------Listing Files in Folder------------ ")

    for file in files:
        print(file.name)

#Tam directorylerin tamamının printini bulup onu da ekleyeceğim

def transferData(file_from, file_to):
    #dbx.files_upload(open(file_from, 'rb').read, file_to)
    with open(file_from, 'rb') as f:
        dbx.files_upload(f.read(), file_to)

file_from = 'deneme.txt'
file_to = '/Deneme/uploadTest.txt'

printSpecifiedDirectory('/Deneme')
#transferData(file_from, file_to)

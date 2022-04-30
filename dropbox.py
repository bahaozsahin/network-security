"""
Backs up and restores a settings file to Dropbox.
This is an example app for API v2.
"""

import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

from csv import writer
import pandas as pd

import requests
import json

app_key = "ph2b2jh4dqjxnew"
app_secret = "ixtrd7ua9h8hr3z"

# build the authorization URL:
authorization_url = "https://www.dropbox.com/oauth2/authorize?client_id=%s&response_type=code" % app_key

# send the user to the authorization URL:
print("Go to the following URL and allow access:")
print(authorization_url)

# get the authorization code from the user:
authorization_code = input('Enter the code:\n')

# exchange the authorization code for an access token:
token_url = "https://api.dropboxapi.com/oauth2/token"
params = {
    "code": authorization_code,
    "grant_type": "authorization_code",
    "client_id": app_key,
    "client_secret": app_secret
}
r = requests.post(token_url, data=params)
data = r.json()
#print(r.text)
#print()
#nCwBrGXp8UgAAAAAAAAAHjSwqRPWuOBy5gpbrou9anU
tokenid=data["access_token"]

tokenurl = "https://api.dropboxapi.com/2/check/user"

headers = {
    "Authorization": "Bearer "+tokenid,
    "Content-Type": "application/json"
}
params = {}

r = requests.post(token_url, data=params)
print(r.text)




url = "https://api.dropboxapi.com/2/file_requests/list"

headers = {
    "Authorization": "Bearer "+tokenid,
    "Content-Type": "application/json"
}

data = None

r = requests.post(url, headers=headers, data=json.dumps(data))

print(r.text)


url = "https://api.dropboxapi.com/2/files/list_folder"

headers = {
    "Authorization": "Bearer "+tokenid,
    "Content-Type": "application/json"
}

data = {
    "path": ""
}

r = requests.post(url, headers=headers, data=json.dumps(data))

data = r.json()
for i in data["entries"]:
    print(i["path_lower"])



def sharingAddFolderMember():
    url = "https://api.dropboxapi.com/2/sharing/add_folder_member"

    headers = {
        "Authorization": "Bearer "+tokenid,
        "Content-Type": "application/json"
    }

    data = {
        "shared_folder_id": "sharedfolderid",
        "members": [{"member":{".tag":"email","email":"dropbox2@haxballplayers.com"},"access_level":{".tag":"owner"}}],
        "custom_message": "custommessage"
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))

    print(r.text)




LOCALFILE = 'C:\\Users\\celal\\Desktop\\deneme1.txt'
BACKUPPATH = '/deneme1.txt'



# Uploads contents of LOCALFILE to Dropbox
def backup():
    with open(LOCALFILE, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
        try:
            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()

# Change the text string in LOCALFILE to be new_content
# @param new_content is a string
def change_local_file(new_content):
    print("Changing contents of " + LOCALFILE + " on local machine...")
    with open(LOCALFILE, 'wb') as f:
        f.write(new_content)

# Restore the local and Dropbox files to a certain revision
def restore(rev=None):
    # Restore the file on Dropbox to a certain revision
    print("Restoring " + BACKUPPATH + " to revision " + rev + " on Dropbox...")
    dbx.files_restore(BACKUPPATH, rev)

    # Download the specific revision of the file at BACKUPPATH to LOCALFILE
    print("Downloading current " + BACKUPPATH + " from Dropbox, overwriting " + LOCALFILE + "...")
    dbx.files_download_to_file(LOCALFILE, BACKUPPATH, rev)

# Look at all of the available revisions on Dropbox, and return the oldest one
def select_revision():
    # Get the revisions for a file (and sort by the datetime object, "server_modified")
    print("Finding available revisions on Dropbox...")
    entries = dbx.files_list_revisions(BACKUPPATH, limit=30).entries
    revisions = sorted(entries, key=lambda entry: entry.server_modified)

    for revision in revisions:
        print(revision.rev, revision.server_modified)

    # Return the oldest revision (first entry, because revisions was sorted oldest:newest)
    return revisions[0].rev

if __name__ == '__main__':
    # Check for an access token
    if (len(tokenid) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token. "
            "Open up backup-and-restore-example.py in a text editor and "
            "paste in your token in line 14.")



    with dropbox.Dropbox(tokenid) as dbx:

        # Check that the access token is valid
        try:
            print(" ")
            #print(dbx.users_get_current_account())

        except AuthError:
            sys.exit("ERROR: Invalid access token; try re-generating an "
                "access token from the app console on the web.")







def deneme():
    # Create a backup of the current settings file
    backup()

    # Change the user's file, create another backup
    change_local_file(b"updated")
    backup()

    # Restore the local and Dropbox files to a certain revision
    to_rev = select_revision()
    restore(to_rev)

    print("Done!")

def add_Friends(name,mail,publickey,filename):
    list_data=[]
    list_data.append(name,mail,publickey,filename)
    with open('friendlist.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list_data)
        f_object.close()

def read_Data():
    data=pd.read_csv("DATA.csv")
    print( data.head())
    data.info()

    y=data["totalDuration"]
    x=data.drop("totalDuration",axis=1)


def createFile():
    url = "https://api.dropboxapi.com/2/files/create_folder_v2"

    headers = {
        "Authorization": "Bearer " + tokenid,
        "Content-Type": "application/json"
    }

    data = {
        "path": "/denemeasd"
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))

    print("Dosya Açma: " + r.text)


def addFileMember():
    url = "https://api.dropboxapi.com/2/sharing/add_file_member"

    headers = {
        "Authorization": "Bearer " + tokenid,
        "Content-Type": "application/json"
    }

    data = {
        "file": "/denemeasd",
        "members": [{".tag": "email", "email": "dropbox2@haxballplayers.com"}],
        "custom_message": "denememesaj",
        "access_level": {".tag": "owner"}
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))
    print("Dosya: " + r.text)


def sharingListFolders():
    url = "https://api.dropboxapi.com/2/sharing/list_folders"

    headers = {
        "Authorization": "Bearer "+tokenid,
        "Content-Type": "application/json"
    }

    data = {
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))
    data = r.json()
    print(data)

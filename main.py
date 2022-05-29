import tkinter as tk
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import ttk
from tkinter import *
from csv import writer
import pandas as pd
from tkinter import filedialog
import os
import webbrowser
import requests
import json
import dropbox
import time
import datetime
import sCrypt
from os import urandom

#Takım
team_member_id=""
mymail="mert_6198@hotmail.com"
TreeviewRootId=""
TreeviewReset=0
TreeviewRootIdDropbox=""
TreeviewResetDropbox=0
TreeviewRootIdFriendList=""
TreeviewResetFriendList=0

checklistlocal=[]
checklistfriends=[]
checklistDropbox=[]

app_key = "y2cmlfwgnv6hsc5"
app_secret = "1iaxpkqwt1gxfwu"

app_key2="gdwqiosu2zbk1zt"
app_secret2="vl7wxyrscrdv0dx"
# build the authorization URL:
authorization_url = "https://www.dropbox.com/oauth2/authorize?client_id=%s&response_type=code" % app_key
authorization_code=""
authorization_url2 = "https://www.dropbox.com/oauth2/authorize?client_id=%s&response_type=code" % app_key2
authorization_code2=""
tokenid=""
tokenid2=""
dbx=dropbox.Dropbox



class CheckboxTreeviewLocalApp(ttk.Treeview):

    def __init__(self, master=None, **kw):
        ttk.Treeview.__init__(self, master,style='Checkbox.Treeview', **kw)
        self.column("#0", width="400")
        self.heading("#0", text="Local DropboxApp")
        style = ttk.Style(self)
        #print(style.theme_names())
        style.theme_use("xpnative")
        style.configure('Checkbox.Treeview', padding=5)
        style.map("Checkbox.Treeview",
                  fieldbackground=[("disabled", '#E6E6E6')],
                  foreground=[("disabled", 'gray40')],
                  background=[("disabled", '#E6E6E6')],
                  )
        style.map("Text",
                  fieldbackground=[("disabled", '#E6E6E6')],
                  foreground=[("disabled", 'gray40')],
                  background=[("disabled", '#E6E6E6')]
                  )




        self.pack()
        # checkboxes are implemented with pictures
        self.im_checked = tk.PhotoImage(file='assets/checked.png')
        self.im_unchecked = tk.PhotoImage(file='assets/unchecked.png')
        self.im_tristate = tk.PhotoImage(file='assets/tristate.png')

        self.tag_configure("unchecked", image=self.im_unchecked)
        self.tag_configure("tristate", image=self.im_tristate)
        self.tag_configure("checked", image=self.im_checked)

        # check / uncheck boxes on click
        self.bind("<Button-1>", self.box_click, True)




    def insert(self, parent, index, iid=None, **kw):
        """ same method as for standard treeview but add the tag 'unchecked'
            automatically if no tag among ('checked', 'unchecked', 'tristate')
            is given """
        global TreeviewRootId
        global TreeviewReset


        if not "tags" in kw:
            kw["tags"] = ("unchecked",)
        elif not ("unchecked" in kw["tags"] or "checked" in kw["tags"]
                  or "tristate" in kw["tags"]):
            kw["tags"] = ("unchecked",)
        if(TreeviewReset==0):
            TreeviewRootId=iid
            TreeviewReset=1


        ttk.Treeview.insert(self, parent, index, iid, **kw)




    def check_descendant(self, item):
        """ check the boxes of item's descendants """
        children = self.get_children(item)
        for iid in children:
            self.item(iid, tags=("checked",))
            self.check_descendant(iid)

    def sync1(self, item):
        print(item)
        original_name = self.item(item, "text")
        if (original_name[0] != "✅"):
            self.item(item, text="✅ " + original_name)

    def sync2(self, item):
        print(item)
        original_name = self.item(item, "text")
        if (original_name[0] != "🔴"):
            self.item(item, text="🔴 " + original_name)

    def sync3(self, item):
        print(item)
        original_name = self.item(item, "text")
        if (original_name[0] != "❌"):
            self.item(item, text="❌ " + original_name)

    def sync4(self, item):
        print(item)
        original_name = self.item(item, "text")
        if (original_name[0] != "🗑️"):
            self.item(item, text="🗑️ " + original_name)

    def check_ancestor(self, item):
        """ check the box of item and change the state of the boxes of item's
            ancestors accordingly """
        self.item(item, tags=("checked",))
        parent = self.parent(item)
        if parent:
            children = self.get_children(parent)
            b = ["checked" in self.item(c, "tags") for c in children]
            if False in b:
                # at least one box is not checked and item's box is checked
                self.tristate_parent(parent)

            else:
                # all boxes of the children are checked
                self.check_ancestor(parent)


    def tristate_parent(self, item):
        """ put the box of item in tristate and change the state of the boxes of
            item's ancestors accordingly """
        self.item(item, tags=("tristate",))
        parent = self.parent(item)
        if parent:
            self.tristate_parent(parent)


    def uncheck_descendant(self, item):
        """ uncheck the boxes of item's descendant """
        children = self.get_children(item)
        for iid in children:
            self.item(iid, tags=("unchecked",))
            self.uncheck_descendant(iid)


    def uncheck_ancestor(self, item):
        """ uncheck the box of item and change the state of the boxes of item's
            ancestors accordingly """
        self.item(item, tags=("unchecked",))
        parent = self.parent(item)
        if parent:
            children = self.get_children(parent)
            b = ["unchecked" in self.item(c, "tags") for c in children]
            if False in b:
                # at least one box is checked and item's box is unchecked
                self.tristate_parent(parent)

            else:
                # no box is checked
                self.uncheck_ancestor(parent)


    def box_click(self, event):
        """ check or uncheck box when clicked """
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        if "image" in elem:
            # a box was clicked
            item = self.identify_row(y)

            tags = self.item(item, "tags")
            if ("unchecked" in tags) or ("tristate" in tags):
                self.check_ancestor(item)
                self.check_descendant(item)
            else:
                self.uncheck_descendant(item)
                self.uncheck_ancestor(item)
            self.checkedList(TreeviewRootId)


    def checkedList(self,root):
        global checklistlocal
        checklistlocal.clear()
        children = self.get_children(root)
        for item in children:
            tags = self.item(item, "tags")
            if("checked" in tags):
                checklistlocal.append(item)
            self.checkedListSelf(item)

    def checkedListSelf(self, root):
        global checklistlocal
        children = self.get_children(root)
        for item in children:
            tags = self.item(item, "tags")
            if ("checked" in tags):
                checklistlocal.append(item)
            self.checkedListSelf(item)

class CheckboxFriendList(ttk.Treeview):

    def __init__(self, master=None, **kw):
        ttk.Treeview.__init__(self, master,style='Checkbox.Treeview', **kw)
        self.column("#0", width="400")
        self.heading("#0", text="Friend List")
        style = ttk.Style(self)
        #print(style.theme_names())
        style.theme_use("xpnative")
        style.configure('Checkbox.Treeview', padding=5)
        style.map("Checkbox.Treeview",
                  fieldbackground=[("disabled", '#E6E6E6')],
                  foreground=[("disabled", 'gray40')],
                  background=[("disabled", '#E6E6E6')],
                  )
        style.map("Text",
                  fieldbackground=[("disabled", '#E6E6E6')],
                  foreground=[("disabled", 'gray40')],
                  background=[("disabled", '#E6E6E6')]
                  )




        self.pack()
        # checkboxes are implemented with pictures
        self.im_checked = tk.PhotoImage(file='assets/checked.png')
        self.im_unchecked = tk.PhotoImage(file='assets/unchecked.png')
        self.im_tristate = tk.PhotoImage(file='assets/tristate.png')

        self.tag_configure("unchecked", image=self.im_unchecked)
        self.tag_configure("tristate", image=self.im_tristate)
        self.tag_configure("checked", image=self.im_checked)

        # check / uncheck boxes on click
        self.bind("<Button-1>", self.box_click, True)




    def insert(self, parent, index, iid=None, **kw):
        """ same method as for standard treeview but add the tag 'unchecked'
            automatically if no tag among ('checked', 'unchecked', 'tristate')
            is given """
        global TreeviewRootIdFriendList
        global TreeviewResetFriendList


        if not "tags" in kw:
            kw["tags"] = ("unchecked",)
        elif not ("unchecked" in kw["tags"] or "checked" in kw["tags"]
                  or "tristate" in kw["tags"]):
            kw["tags"] = ("unchecked",)
        if(TreeviewResetFriendList==0):
            TreeviewRootIdFriendList=iid
            TreeviewResetFriendList=1


        ttk.Treeview.insert(self, parent, index, iid, **kw)




    def check_descendant(self, item):
        """ check the boxes of item's descendants """
        children = self.get_children(item)
        for iid in children:
            self.item(iid, tags=("checked",))
            self.check_descendant(iid)



    def check_ancestor(self, item):
        """ check the box of item and change the state of the boxes of item's
            ancestors accordingly """
        self.item(item, tags=("checked",))
        parent = self.parent(item)
        if parent:
            children = self.get_children(parent)
            b = ["checked" in self.item(c, "tags") for c in children]
            if False in b:
                # at least one box is not checked and item's box is checked
                self.tristate_parent(parent)

            else:
                # all boxes of the children are checked
                self.check_ancestor(parent)


    def tristate_parent(self, item):
        """ put the box of item in tristate and change the state of the boxes of
            item's ancestors accordingly """
        self.item(item, tags=("tristate",))
        parent = self.parent(item)
        if parent:
            self.tristate_parent(parent)


    def uncheck_descendant(self, item):
        """ uncheck the boxes of item's descendant """
        children = self.get_children(item)
        for iid in children:
            self.item(iid, tags=("unchecked",))
            self.uncheck_descendant(iid)


    def uncheck_ancestor(self, item):
        """ uncheck the box of item and change the state of the boxes of item's
            ancestors accordingly """
        self.item(item, tags=("unchecked",))
        parent = self.parent(item)
        if parent:
            children = self.get_children(parent)
            b = ["unchecked" in self.item(c, "tags") for c in children]
            if False in b:
                # at least one box is checked and item's box is unchecked
                self.tristate_parent(parent)

            else:
                # no box is checked
                self.uncheck_ancestor(parent)


    def box_click(self, event):
        """ check or uncheck box when clicked """
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        if "image" in elem:
            # a box was clicked
            item = self.identify_row(y)
            tags = self.item(item, "tags")
            if ("unchecked" in tags) or ("tristate" in tags):
                self.check_ancestor(item)
                self.check_descendant(item)
            else:
                self.uncheck_descendant(item)
                self.uncheck_ancestor(item)
            self.checkedList(TreeviewRootIdFriendList)


    def checkedList(self,root):
        global checklistfriends
        checklistfriends.clear()
        children = self.get_children(root)
        for item in children:
            tags = self.item(item, "tags")
            if("checked" in tags):
                checklistfriends.append(item)
            self.checkedListSelf(item)

    def checkedListSelf(self, selfroot):
        global checklistfriends
        children = self.get_children(selfroot)
        for item in children:
            tags = self.item(item, "tags")
            if ("checked" in tags):
                checklistfriends.append(item)
            self.checkedListSelf(item)



class CheckboxTreeviewDropboxApp(ttk.Treeview):

    def __init__(self, master=None, **kw):
        ttk.Treeview.__init__(self, master,style='Checkbox.Treeview', **kw)
        self.column("#0", width="400")
        self.heading("#0", text="DropboxApp")
        style = ttk.Style(self)
        #print(style.theme_names())
        style.theme_use("xpnative")
        style.configure('Checkbox.Treeview', padding=5)
        style.map("Checkbox.Treeview",
                  fieldbackground=[("disabled", '#E6E6E6')],
                  foreground=[("disabled", 'gray40')],
                  background=[("disabled", '#E6E6E6')]
                  )






        self.pack()
        # checkboxes are implemented with pictures
        self.im_checked = tk.PhotoImage(file='assets/checked.png')
        self.im_unchecked = tk.PhotoImage(file='assets/unchecked.png')
        self.im_tristate = tk.PhotoImage(file='assets/tristate.png')

        self.tag_configure("unchecked", image=self.im_unchecked)
        self.tag_configure("tristate", image=self.im_tristate)
        self.tag_configure("checked", image=self.im_checked)

        # check / uncheck boxes on click
        self.bind("<Button-1>", self.box_click, True)




    def insert(self, parent, index, iid=None, **kw):
        """ same method as for standard treeview but add the tag 'unchecked'
            automatically if no tag among ('checked', 'unchecked', 'tristate')
            is given """
        global TreeviewRootIdDropbox
        global TreeviewResetDropbox


        if not "tags" in kw:
            kw["tags"] = ("unchecked",)
        elif not ("unchecked" in kw["tags"] or "checked" in kw["tags"]
                  or "tristate" in kw["tags"]):
            kw["tags"] = ("unchecked",)
        if(TreeviewResetDropbox==0):
            TreeviewRootIdDropbox=iid
            TreeviewResetDropbox=1


        ttk.Treeview.insert(self, parent, index, iid, **kw)




    def check_descendant(self, item):
        """ check the boxes of item's descendants """
        children = self.get_children(item)
        for iid in children:
            self.item(iid, tags=("checked",))
            self.check_descendant(iid)

    def sync1(self,item):
        print(item)
        original_name=self.item(item,"text")
        if(original_name[0]!="✅"):
            self.item(item, text="✅ "+original_name)

    def sync2(self,item):
        print(item)
        original_name=self.item(item,"text")
        if(original_name[0]!="🔴"):
            self.item(item, text="🔴 "+original_name)

    def sync3(self, item):
        print(item)
        original_name = self.item(item, "text")
        if (original_name[0] != "❌"):
            self.item(item, text="❌ " + original_name)

    def check_ancestor(self, item):
        """ check the box of item and change the state of the boxes of item's
            ancestors accordingly """
        self.item(item, tags=("checked",))
        parent = self.parent(item)
        if parent:
            children = self.get_children(parent)
            b = ["checked" in self.item(c, "tags") for c in children]
            if False in b:
                # at least one box is not checked and item's box is checked
                self.tristate_parent(parent)

            else:
                # all boxes of the children are checked
                self.check_ancestor(parent)


    def tristate_parent(self, item):
        """ put the box of item in tristate and change the state of the boxes of
            item's ancestors accordingly """
        self.item(item, tags=("tristate",))
        parent = self.parent(item)
        if parent:
            self.tristate_parent(parent)


    def uncheck_descendant(self, item):
        """ uncheck the boxes of item's descendant """
        children = self.get_children(item)
        for iid in children:
            self.item(iid, tags=("unchecked",))
            self.uncheck_descendant(iid)


    def uncheck_ancestor(self, item):
        """ uncheck the box of item and change the state of the boxes of item's
            ancestors accordingly """
        self.item(item, tags=("unchecked",))
        parent = self.parent(item)
        if parent:
            children = self.get_children(parent)
            b = ["unchecked" in self.item(c, "tags") for c in children]
            if False in b:
                # at least one box is checked and item's box is unchecked
                self.tristate_parent(parent)

            else:
                # no box is checked
                self.uncheck_ancestor(parent)


    def box_click(self, event):
        """ check or uncheck box when clicked """
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        if "image" in elem:
            # a box was clicked
            item = self.identify_row(y)
            tags = self.item(item, "tags")
            if ("unchecked" in tags) or ("tristate" in tags):
                self.check_ancestor(item)
                self.check_descendant(item)
            else:
                self.uncheck_descendant(item)
                self.uncheck_ancestor(item)
            self.checkedList(TreeviewRootIdDropbox)


    def checkedList(self,root):
        global checklistDropbox
        checklistDropbox.clear()
        children = self.get_children(root)
        for item in children:
            tags = self.item(item, "tags")
            if("checked" in tags):
                checklistDropbox.append(item)
            self.checkedListSelf(item)

    def checkedListSelf(self,root):
        children = self.get_children(root)
        for item in children:
            tags = self.item(item, "tags")
            if("checked" in tags):
                checklistDropbox.append(item)
            self.checkedListSelf(item)


def browseLocal():
    global checklistlocal
    checklistlocal.clear()

    treeview=t
    for item in treeview.get_children():
        treeview.delete(item)

    browsedDir="C:/Users/DropboxApp"
    treeview.insert('', 0, browsedDir,text=browsedDir,open=True)


    listSubfolders(browsedDir)
    return (browsedDir)

def listSubfolders(path):

    #dbx= dropbox.Dropbox(tokenid)



    treeview=t
    for p in os.listdir(path):
        sync = 0
        abspath = os.path.join(path, p)

        path = path.replace("\\", "/")
        print(path)
        abspath=abspath.replace("\\", "/")

        fileDropboxPath = abspath[8:]
        file_with_folder = fileDropboxPath
        if os.path.isfile(abspath):
            basename = os.path.basename(abspath)
            print(file_with_folder)
            file_with_folder = fileDropboxPath + "/" + basename
            print("isim değişti")
            print(file_with_folder)

        print(file_with_folder)

        fullname = abspath





        try:
            f = dbx.files_get_metadata(path=file_with_folder, include_deleted=True)
            print(f)

            if isinstance(f, dropbox.files.FileMetadata):
                print("FileMetadata")
                mtime = os.path.getmtime(fullname)

                mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                size = os.path.getsize(fullname)
                print(mtime_dt)
                print(size)

                metadata_client_modified = f.client_modified
                metadata_size = f.size

                print(metadata_client_modified)
                print(metadata_size)
                if (mtime_dt == metadata_client_modified and size == metadata_size):
                    print("Senkron" + fileDropboxPath)

                    sync = 1
                else:
                    print("Senkron Değil:" + fileDropboxPath)

                    sync = 2
            if isinstance(f, dropbox.files.FolderMetadata):
                print("FolderMetadata")
                sync=0
            if isinstance(f, dropbox.files.DeletedMetadata):
                print("DeletedMetadata")
                sync=4
        except Exception as e:
            sync=3
            print("Dosya Yok")





        #metadata=getMetaData(fileDropboxPath)








        if(treeview.exists(abspath)==False):
            treeview.insert(path, "end", abspath, text=p,open=True)

        if (sync == 1):
            treeview.sync1(fullname)
            #Var ve Senkron
        if (sync == 2):
            treeview.sync2(fullname)
            #Var ama Senkron Değil
        if (sync == 3):
            treeview.sync3(fullname)
            #Bulunmayan
        if (sync == 4):
            treeview.sync4(fullname)
            #Silinmiş

        t.pack()

        if os.path.isdir(abspath):
            listSubfolders(abspath)



def browseDropbox():

    global checklistDropbox
    checklistDropbox.clear()

    treeview=tdrop
    for item in treeview.get_children():
        treeview.delete(item)

    browsedDir="DropboxApp"

    treeview.insert('', 0, "DropboxApp",text=browsedDir,open=True)

    #onDoubleClick() fonksiyonunu ekleme
    #treeview.bind("<Double-Button-1>", onDoubleClick)

    #browseShared()
    listSubfoldersDropbox("/DropboxApp","DropboxApp")
    return (browsedDir)



def listSubfoldersDropbox(path,parent):



    treeview=tdrop

    try:


        for p in dbx.files_list_folder(path).entries:
            sync = 0
            visible=0
            childsize = 0
            nameequal = 0
            lastfile=0
            try:
                if(p.sharing_info.no_access==False):
                    visible=1
            except:
                visible=1


            if(visible==1):


                for p2 in dbx.files_list_folder(p.path_lower).entries:
                    childsize+=1
                    if(p2.name==p.name):
                        nameequal=1

                fullname = "C:/Users" + p.path_lower
                filepathname=fullname
                dropboxpath=p.path_lower
                if(childsize==1 and nameequal==1):
                    filepathname = "C:/Users" + p.path_lower+"/"+p.name
                    dropboxpath = p.path_lower+"/"+p.name
                    lastfile=1

                print(os.path.basename(fullname))

                if (os.path.exists(fullname)):
                    try:


                        mtime = os.path.getmtime(fullname)

                        mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])

                        size = os.path.getsize(fullname)

                        print(dropboxpath)
                        metadata=dbx.files_get_metadata(dropboxpath)


                        if(mtime_dt == metadata.client_modified and size == metadata.size):
                            #print("Senkron"+p.path_lower)
                            sync = 1
                        else:
                            #print("Senkron Değil:"+p.path_lower)
                            sync = 2

                    except Exception as e:
                            #print(e)
                            #print("Dosya  Bulunmamaktadır 1 :" + p.path_lower)
                            #Dosya ise ve bulunuyorsa
                            sync=0
                else:
                    sync = 3

                treeview.insert(parent, 'end', dropboxpath, text=p.name, open=True)

                if (sync == 1):
                    treeview.sync1(dropboxpath)
                if (sync == 2):
                    treeview.sync2(dropboxpath)
                if (sync == 3):
                    treeview.sync3(dropboxpath)

                if(lastfile==0):
                    listSubfoldersDropbox(dropboxpath,dropboxpath)
                else:
                    print(p.path_lower+" da girmedim")

    except Exception as e:
        #print("EXCEPT")
        print(e)

def shareFile(file_url,friend_mail,custom_message):

    url = "https://api.dropboxapi.com/2/sharing/add_file_member"

    headers = {
        "Authorization": "Bearer "+tokenid,
        "Content-Type": "application/json"
    }

    data = {
        "file": file_url,
        "members": [{".tag": "email", "email": friend_mail}],
        "custom_message": custom_message
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))

    data = r.json()
    print(data)

def shareFolder(file_url,mail):
    folderid=getFolderId(file_url)
    url = "https://api.dropboxapi.com/2/sharing/add_folder_member"

    headers = {
        "Authorization": "Bearer "+tokenid,
        "Content-Type": "application/json"
    }

    data = {
        "shared_folder_id": folderid,
        "members": [{"member":{".tag":"email","email":mail},"access_level":{".tag":"owner"}}]
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))

    data = r.json()
    print(data)

def getFolderId(file_url):
    a=dbx.files_get_metadata(path=file_url)
    print(a)




def onDoubleClick(event):
    iid = event.widget.focus()
    item = event.widget.item(iid)
    parentDeneme = event.widget.parent(iid)
    values = item['values']
    # print("you clicked on", item)
    newpath = ""
    for values in item['values']:
        newpath += values + " "
    # print("you clicked on", parentDeneme)
    # print(iid)

    # sondaki boşluğu sil
    newpath = newpath[:-1]
    if (newpath != ""):
        newpath += "/" + item['text']
    else:
        newpath = item['text']
    print(newpath)
    global pathForUpload
    pathForUpload = newpath

def writeConsoleMain(*message, end = "\n", sep = " "):
    Console['state'] = 'normal'
    text = ""
    for item in message:
        text += "{}".format(item)
        text += sep
    text += end
    Console.insert(INSERT, text)
    Console['state'] = 'disabled'

def writeConsoleFriend(*message, end = "\n", sep = " "):
    ConsoleFriend['state'] = 'normal'
    text = ""
    for item in message:
        text += "{}".format(item)
        text += sep
    text += end
    ConsoleFriend.insert(INSERT, text)
    ConsoleFriend['state'] = 'disabled'

def writeConsoleLogin(*message, end = "\n", sep = " "):
    ConsoleLogin['state'] = 'normal'
    text = ""
    for item in message:
        text += "{}".format(item)
        text += sep
    text += end
    ConsoleLogin.insert(INSERT, text)
    ConsoleLogin['state'] = 'disabled'

def add_Friends():
    global FriendName
    global FriendMail
    global FriendPublicKey

    name=FriendName.get()
    mail = FriendMail.get()
    publickey = FriendPublicKey.get()
    print(name)
    if(name!="" and mail!="" and publickey!=""):
        list_data=[name,mail,publickey]
        with open('friendlist.csv', 'a', newline='') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(list_data)
            writeConsoleFriend(name+" Kişisi Başarıyla Eklendi")
            f_object.close()
    else:
        writeConsoleFriend("Bilgiler Boş Olamaz Kişiler Eklenemedi")

    FriendName.delete(0, tk.END)
    FriendName.insert(0, "")
    FriendMail.delete(0, tk.END)
    FriendMail.insert(0, "")
    FriendPublicKey.delete(0, tk.END)
    FriendPublicKey.insert(0, "")

def read_Friends():
    global fl
    global friendlistroot
    global checklistfriends
    checklistfriends.clear()

    fl.delete(*fl.get_children())
    friendlistroot = fl.insert('', 0, "friendslistroot", text="All", open=True)
    data=pd.read_csv("friendlist.csv")
    name=data["name"]
    for names in name:
        fl.insert("friendslistroot", "end", names, text=names)




def MainToFriendFrame():
    destroyMainFrame()
    createFriendFrame()

def FriendToMainFrame():
    destroyFriendFrame()
    createMainFrame()

def LoginToMainFrame():
    destroyLoginFrame()
    createMainFrame()

def ResetFriends():
    read_Friends()

def ResetLocalDropbox():
    browseLocal()

def ResetDropbox():
    browseDropbox()

def UploadDropbox():
    for files in checklistlocal:

        if os.path.isfile(files):
            file_from=files
            basename = os.path.basename(file_from)
            file_folder=files[8:]
            file_with_folder=file_folder+"/"+basename

            print(file_folder)
            print(file_with_folder)
            print("Files: "+files)
            UploadFile(files,file_with_folder)
            getFolderId(file_folder)
            #shareFile(files[8:],"dropbox2@haxballplayers.com","deneme132")
           #shareFile(files[19:],"dropbox2@haxballplayers.com","deneme132")

    for friends in checklistfriends:
        print("Friends: "+friends)

    ResetLocalDropbox()
    ResetDropbox()

def DownloadDropbox():
    for files in checklistDropbox:

        try:
            f = dbx.files_get_metadata(path=files, include_deleted=True)
            if isinstance(f, dropbox.files.FileMetadata):
                print("İndirilmek istenen dosya: "+files)
                DownloadFile(files)
        except Exception as e:
            print(e)


    ResetLocalDropbox()
    ResetDropbox()

def UploadFile(file_from,file_to):
    try:

        #dbx=dropbox.Dropbox(tokenid)

        mtime = os.path.getmtime(file_from)
        #print("Upload")
        #print(mtime)
        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to,mode=dropbox.files.WriteMode.overwrite,client_modified=datetime.datetime(*time.gmtime(mtime)[:6]))

        writeConsoleMain(file_to+" Upload Successful")
        print(file_to + " Upload Successful")

    except Exception as e:
        writeConsoleMain(e)


def DownloadFile(file_from):
    #dbx=dropbox.Dropbox(tokenid)


    #file_to = "C:/Users/DropboxApp" + file_from  # + file_name[-1]
    file_to = "C:/Users" + file_from  # + file_name[-1]                    dosya
    print(file_to)
    print(file_from)
    file_to=file_to.split('/')
    file_to.pop() #skip same with file name
    path_download=""
    count=0
    for paths in file_to:
        if(count!=0):
            path_download+="/"
        path_download+=paths
        count += 1

    print("SON indirilme yeri:"+path_download)


    #print(file_to)
    file_hierarchy_check = path_download.split('/')  # dosyaarray
    file_hierarchy_check.pop(0)  # for skipping the check for C: directory and Users
    file_hierarchy_check.pop(0)
    file_hierarchy_check.pop()  # skipping the check for the file that will be created

    current_folder = "C:/Users/"  # konum
    #print(file_hierarchy_check)

    for file in file_hierarchy_check:
        #print(file)
        file_to_create = current_folder + file
        #print(file_to_create)
        if not os.path.exists(file_to_create):
            print("Creating folder according to your Dropbox file hierarchy")
            os.mkdir(file_to_create)
        else:
            print("Folder alredy exists")
        current_folder = file_to_create + "/"
    #path_download = "C:/Users/DropboxApp" + file_from




    dbx.files_download_to_file(download_path=path_download, path=file_from)

    #os.utime(file_to, (access_time, modification_time))
    writeConsoleMain('Download successful '+path_download)
    print('Download successful '+path_download)


def callback(url):
    webbrowser.open_new(url)

def getMetaData(path):
    url = "https://api.dropboxapi.com/2/files/get_metadata"

    headers = {
        "Authorization": "Bearer "+tokenid,
        "Content-Type": "application/json"
    }

    data = {
        "path": path,
        "include_media_info": True,
        "include_deleted": True,
        "include_has_explicit_shared_members": True,
        "Dropbox-Api-Select-User": team_member_id
    }

    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(r)
    data = r.json()
    return data

def Login2():
    global  authorization_code2
    global tokenid2
    global dbx

    login=0
    authorization_code2=LoginAuthorizationCode2.get()
    token_url = "https://api.dropboxapi.com/oauth2/token"
    params = {
        "code": authorization_code2,
        "grant_type": "authorization_code",
        "client_id": app_key2,
        "client_secret": app_secret2
    }
    r = requests.post(token_url, data=params)

    data = r.json()
    try:
        if(data["error_description"]!=""):
            writeConsoleLogin(data["error_description"])
    except:
        try:
            if(data["access_token"] != ""):
                tokenid2 = data["access_token"]
                writeConsoleLogin("Başarıyla Giriş Yapıldı")
                print(tokenid)
                time.sleep(1)
                login=1
        except:
                writeConsoleLogin("Hata access_token Bulunamadı")

    if (login==1):
        dbx=dropbox.Dropbox(tokenid2)
        Login()



def Login():
    global  authorization_code
    global tokenid
    global dbx

    login=0
    authorization_code=LoginAuthorizationCode.get()
    token_url = "https://api.dropboxapi.com/oauth2/token"
    params = {
        "code": authorization_code,
        "grant_type": "authorization_code",
        "client_id": app_key,
        "client_secret": app_secret
    }
    r = requests.post(token_url, data=params)

    data = r.json()
    try:
        if(data["error_description"]!=""):
            writeConsoleLogin(data["error_description"])
    except:
        try:
            if(data["access_token"] != ""):
                tokenid = data["access_token"]
                writeConsoleLogin("Başarıyla Giriş Yapıldı")
                print(tokenid)
                time.sleep(1)
                login=1
        except:
                writeConsoleLogin("Hata access_token Bulunamadı")

    if (login==1):
        #dbx=dropbox.Dropbox(tokenid)
       # dbx.DropboxTeam(tokenid).as_user("dbmid:AAAPamqUhqmkb33V3tXvMZnO9WDdLxo_3L4").files_list_folder("").entries
        #Takım
        #FullAccount(account_id='dbid:AAC_I_3x8l6Wxi0VA74fQ_CCUH_58qtXWEY',
        # account_type=AccountType('business', None), country='TR', disabled=False, email='mert_1998_61@hotmail.com',
        # email_verified=True, is_paired=False, locale='en', name=Name(abbreviated_name='MO', display_name='Mert Onur',
        # familiar_name='Mert', given_name='Mert', surname='Onur'), profile_photo_url=NOT_SET,
        # referral_link='https://www.dropbox.com/referrals/AACCXIWBQhuLKGCzMD_IFTNm7woWyYAEleA?src=app9-3005985',
        # root_info=TeamRootInfo(home_namespace_id='2580636065', home_path='/Mert Onur', root_namespace_id='2580493889')
        # , team=FullTeam(id='dbtid:AACvvp0qGYyXmzSxNGKidculbQReHO01VYs', name='Team', office_addin_policy=OfficeAddInPolicy('enabled', None),
        # sharing_policies=TeamSharingPolicies(shared_folder_join_policy=SharedFolderJoinPolicy('from_anyone', None),
        # shared_folder_member_policy=SharedFolderMemberPolicy('anyone', None), shared_link_create_policy=SharedLinkCreatePolicy('default_public', None))),
        # team_member_id='dbmid:AAAPamqUhqmkb33V3tXvMZnO9WDdLxo_3L4')
        dbx.users_get_current_account()
        mymail = dbx.users_get_current_account().email
        print(mymail + " mymail")
        root_namespace_id = dbx.users_get_current_account().root_info.root_namespace_id
        print(root_namespace_id + " root_namespace_id")
        team_member_id=dbx.users_get_current_account().team_member_id
        print(dbx.users_get_current_account())

        dbx=dropbox.DropboxTeam(tokenid).with_path_root(dropbox.common.PathRoot.root(root_namespace_id)).as_user(team_member_id)

        #headers = {
        #    "Content-Type": "application/json",
        #    "Dropbox-Api-Select-User": team_member_id
        #}
        #dbx=dropbox.Dropbox(oauth2_access_token=tokenid,headers=headers)

        LoginToMainFrame()




root = tk.Tk()
root.title('DropboxApp')
root.geometry('1510x800')
LoginFrame=tk.Frame(root, width=1510, height=800, relief='raised', borderwidth=5)
MainFrame= tk.Frame(root, width=1510, height=800, relief='raised', borderwidth=5)
FriendFrame=tk.Frame(root, width=1510, height=800, relief='raised', borderwidth=5)

LoginPageButton = tk.Button(LoginFrame, text='Login', command=add_Friends, relief='raised', borderwidth=5)
ConsoleLogin = Text(LoginFrame)
LoginAuthorizationCode = tk.Entry(LoginFrame)
LoginAuthorizationCodeLabel = tk.Label(LoginFrame)
LoginAuthorizationCode2 = tk.Entry(LoginFrame)
LoginAuthorizationCodeLabel2 = tk.Label(LoginFrame)


treeviewLocal= ttk.Treeview(MainFrame)
t=CheckboxTreeviewLocalApp(treeviewLocal,height=20)
treeviewDropbox= ttk.Treeview(MainFrame)
tdrop=CheckboxTreeviewDropboxApp(treeviewDropbox,height=20)

FriendListTreeview = ttk.Treeview(MainFrame)
fl = CheckboxFriendList(FriendListTreeview, height=20)
friendlistroot=fl.insert('', 0, "friendslistroot",text="Friends List",open=True)
Console = Text(MainFrame)
FriendPageButton = tk.Button(MainFrame, text='Add Friend',command=MainToFriendFrame,relief='raised' ,borderwidth=5)
ResetFriendsButton = tk.Button(MainFrame, text='Refresh Friends',command=ResetFriends,relief='raised' ,borderwidth=5)
ResetLocalDropboxButton = tk.Button(MainFrame, text='Refresh Local Files',command=ResetLocalDropbox,relief='raised' ,borderwidth=5)
ResetDropboxButton= tk.Button(MainFrame, text='Refresh Dropbox Files',command=ResetDropbox,relief='raised' ,borderwidth=5)
UploadButton = tk.Button(MainFrame, text='Upload',command=UploadDropbox,relief='raised' ,borderwidth=5)
DownloadButton = tk.Button(MainFrame, text='Download',command=DownloadDropbox,relief='raised' ,borderwidth=5)

MainPageButton = tk.Button(FriendFrame, text='Main Page', command=FriendToMainFrame, relief='raised',borderwidth=5)
FriendName = tk.Entry(FriendFrame)
FriendMail = tk.Entry(FriendFrame)
FriendPublicKey = tk.Entry(FriendFrame)
ConsoleFriend = Text(FriendFrame)


def createLoginFrame():
    global root
    global LoginFrame
    global LoginPageButton
    global ConsoleLogin
    global LoginAuthorizationCode
    global LoginAuthorizationCodeLabel
    global LoginAuthorizationCode2
    global LoginAuthorizationCodeLabel2

    LoginFrame = tk.Frame(root, width=1510, height=800, relief='raised', borderwidth=5)
    LoginFrame.pack()

    LoginPageButton = tk.Button(LoginFrame, text='Login', command=Login2, relief='raised', borderwidth=5)
    LoginPageButton.place(x=130, y=220 ,width=100, height=25)

    ConsoleLogin = Text(LoginFrame)
    ConsoleLogin.pack()
    ConsoleLogin['state'] = 'disabled'

    ConsoleLogin.place(x=850,y=10)

    LoginAuthorizationCode = tk.Entry(LoginFrame)
    LoginAuthorizationCode["borderwidth"] = "1px"
    LoginAuthorizationCode["text"] = ""
    LoginAuthorizationCode.place(x=130, y=80, width=400, height=25)

    LoginAuthorizationCodeLabel = tk.Label(LoginFrame)
    LoginAuthorizationCodeLabel["justify"] = "center"
    LoginAuthorizationCodeLabel["text"] = "Authorization Code"
    LoginAuthorizationCodeLabel.place(x=10, y=80, width=120, height=25)

    link = Label(LoginFrame, text="Click For Authorization Code", fg="blue", cursor="hand2")
    link.place(x=100, y=40, width=200, height=25)
    link.bind("<Button-1>", lambda e: callback(authorization_url))

    LoginAuthorizationCode2 = tk.Entry(LoginFrame)
    LoginAuthorizationCode2["borderwidth"] = "1px"
    LoginAuthorizationCode2["text"] = ""
    LoginAuthorizationCode2.place(x=130, y=160, width=400, height=25)

    LoginAuthorizationCodeLabel2 = tk.Label(LoginFrame)
    LoginAuthorizationCodeLabel2["justify"] = "center"
    LoginAuthorizationCodeLabel2["text"] = "Authorization Code"
    LoginAuthorizationCodeLabel2.place(x=10, y=160, width=120, height=25)

    link = Label(LoginFrame, text="Click For Authorization Code", fg="blue", cursor="hand2")
    link.place(x=100, y=120, width=200, height=25)
    link.bind("<Button-1>", lambda e: callback(authorization_url2))


def destroyLoginFrame():
    global LoginFrame
    LoginFrame.destroy()

def createMainFrame():
    global root
    global MainFrame
    global treeviewLocal
    global t
    global treeviewDropbox
    global tdrop
    global FriendListTreeview
    global fl
    global Console
    global FriendPageButton
    global ResetFriendsButton
    global ResetLocalDropboxButton
    global ResetDropboxButton
    global UploadButton
    global DownloadButton

    MainFrame = tk.Frame(root, width=1510, height=800, relief='raised', borderwidth=5)
    MainFrame.pack()




    treeviewLocal = ttk.Treeview(MainFrame)
    treeviewLocal.place(x=10, y=10, width=410)
    t=CheckboxTreeviewLocalApp(treeviewLocal,height=15)
    t.pack()

    treeviewDropbox = ttk.Treeview(MainFrame)
    treeviewDropbox.place(x=10, y=390, width=410)
    tdrop = CheckboxTreeviewDropboxApp(treeviewDropbox, height=15)
    tdrop.pack()


    FriendListTreeview = ttk.Treeview(MainFrame)
    FriendListTreeview.place(x=430, y=10, width=410)
    fl = CheckboxFriendList(FriendListTreeview, height=15)
    fl.pack()

    ResetFriendsButton = tk.Button(MainFrame, text='Refresh Friends', command=ResetFriends, relief='raised',
                                   borderwidth=5)
    ResetFriendsButton.place(x=430, y=350)
    ResetLocalDropboxButton = tk.Button(MainFrame, text='Refresh Local Files', command=ResetLocalDropbox,
                                        relief='raised', borderwidth=5)
    ResetLocalDropboxButton.place(x=70, y=350)

    ResetDropboxButton = tk.Button(MainFrame, text='Refresh Dropbox Files', command=ResetDropbox,
                                        relief='raised', borderwidth=5)
    ResetDropboxButton.place(x=100, y=730)

    UploadButton = tk.Button(MainFrame, text='Upload', command=UploadDropbox, relief='raised', borderwidth=5)
    UploadButton.place(x=10, y=350)
    DownloadButton = tk.Button(MainFrame, text='Download', command=DownloadDropbox, relief='raised', borderwidth=5)
    DownloadButton.place(x=10, y=730)


    Console = Text(MainFrame)
    Console.pack()
    Console['state'] = 'disabled'

    Console.place(x=850,y=10)

    #,command=MainToFriendFrame
    FriendPageButton = tk.Button(MainFrame, text='Add Friend',command=MainToFriendFrame,relief='raised' ,borderwidth=5)
    FriendPageButton.place(x=550,y=350)

    browseLocal()
    read_Friends()
    browseDropbox()



def destroyMainFrame():
    global MainFrame
    MainFrame.destroy()

def createFriendFrame():
    global root
    global FriendFrame
    global MainPageButton
    global FriendName
    global FriendMail
    global FriendPublicKey
    global ConsoleFriend

    FriendFrame = tk.Frame(root, width=1510, height=800, relief='raised', borderwidth=5)
    FriendFrame.pack()
    MainPageButton = tk.Button(FriendFrame, text='Main Page', command=FriendToMainFrame, relief='raised',borderwidth=5)
    MainPageButton.place(x=10, y=750)

    FriendName = tk.Entry(FriendFrame)
    FriendName["borderwidth"] = "1px"
    FriendName["text"] = ""
    FriendName.place(x=100, y=10, width=200, height=25)

    FriendNameLabel = tk.Label(FriendFrame)
    FriendNameLabel["justify"] = "center"
    FriendNameLabel["text"] = "Name"
    FriendNameLabel.place(x=10, y=10, width=70, height=25)

    FriendMail = tk.Entry(FriendFrame)
    FriendMail["borderwidth"] = "1px"
    FriendMail["text"] = ""
    FriendMail.place(x=100, y=45, width=200, height=25)

    FriendMailLabel = tk.Label(FriendFrame)
    FriendMailLabel["justify"] = "center"
    FriendMailLabel["text"] = "Mail"
    FriendMailLabel.place(x=10, y=45, width=70, height=25)

    FriendPublicKey = tk.Entry(FriendFrame)
    FriendPublicKey["borderwidth"] = "1px"
    FriendPublicKey["text"] = ""
    FriendPublicKey.place(x=100, y=80, width=200, height=25)

    FriendPublicKeyLabel = tk.Label(FriendFrame)
    FriendPublicKeyLabel["justify"] = "center"
    FriendPublicKeyLabel["text"] = "Public Key"
    FriendPublicKeyLabel.place(x=10, y=80, width=70, height=25)

    MainPageButton = tk.Button(FriendFrame, text='Add', command=add_Friends, relief='raised', borderwidth=5)
    MainPageButton.place(x=100, y=120 ,width=100, height=25)

    ConsoleFriend = Text(FriendFrame)
    ConsoleFriend.pack()
    ConsoleFriend['state'] = 'disabled'

    ConsoleFriend.place(x=850,y=10)

def sharedLink(link):
    url = "https://content.dropboxapi.com/2/sharing/get_shared_link_file"

    headers = {
        "Authorization": "Bearer sl.BHK2vLYI7h26x4UmSTDaoDobYUxAshLdIjaIG_2VlRh351ool4ZQOIC3m5u53vOdjB362rP957HU46AepYsav-u2VYcb16kj-GGrrCK9va3mfitQaxXS7AjmMBS2xrnfwoCx9RIMMoLC",
        "Dropbox-API-Arg": "{\"url\":\"https://www.dropbox.com/scl/fi/13p6m599sez8g6yr8dy9a/df.py?dl=0\"}"
    }

    r = requests.post(url, headers=headers)


def destroyFriendFrame():
    global FriendFrame
    FriendFrame.destroy()


if __name__ == '__main__':
    #stinfo = os.stat('C:/Users/DropboxApp/aaa/df.py')
    #print(stinfo)

    #dbx=dropbox.Dropbox("sl.BHK2vLYI7h26x4UmSTDaoDobYUxAshLdIjaIG_2VlRh351ool4ZQOIC3m5u53vOdjB362rP957HU46AepYsav-u2VYcb16kj-GGrrCK9va3mfitQaxXS7AjmMBS2xrnfwoCx9RIMMoLC")
    #print(dbx.sharing_list_received_files())
    #print(dbx.sharing_list_folders())
    #for p in dbx.sharing_list_received_files().entries:
     #   print(p)
    #dbx=dropbox
    #tokenid="sl.BHKfFmqzIlNozaqjAW07yzQQ561DnqVeTsNoN1WOXGfdKNJlKQBPVcnddBG4yG8ywnMEpB6vah9bD65hw_4PKLZ6uH0UvnDysQL8dir8QvQauRgMzyrz2VhzNc8dnsNr0iYXfl6_4KfR0kF69UA"
    #print(dbx.DropboxTeam(tokenid).as_admin("dbmid:AAAPamqUhqmkb33V3tXvMZnO9WDdLxo_3L4").files_list_folder("").entries)
    #output = dbx.DropboxTeam(tokenid).with_path_root(dbx.common.PathRoot.root("2580493889")).as_user("dbmid:AAAPamqUhqmkb33V3tXvMZnO9WDdLxo_3L4").files_list_folder("/dropboxapp").entries
    #output = dbx.DropboxTeam(tokenid).with_path_root(dbx.common.PathRoot.root("2580493889")).as_user("dbmid:AAAPamqUhqmkb33V3tXvMZnO9WDdLxo_3L4").files_list_folder("/dropboxapp").entries

    #print(output)
    #dbx=dropbox.DropboxTeam(tokenid).with_path_root(dbx.common.PathRoot.root("2580493889")).as_user("dbmid:AAAPamqUhqmkb33V3tXvMZnO9WDdLxo_3L4")
    #print(dbx.files_download_to_file(download_path="C:/Users/celal/Desktop/indiryuklesil/h7.pdf", path="/dropboxapp/h7.pdf"))
    #DownloadFile("/dropboxapp/h7.pdf")
    createLoginFrame()
    #dbx.sharing
    maillist=["asdfas@gmail.com","mert_6198@hotmail.com","mert_1998_61@hotmail.com"]
    #sCrypt.Asymmetric_Key_Generating()
    sCrypt.Asymmetric_Key_Reading()
    key = urandom(16)
    iv = urandom(16)
    mac_key = urandom(16)
    auth = sCrypt.encrypt_then_mac('C:/Users/pc/Desktop/denemee.txt', iv, key, mac_key, 16)
    print("Auth:" + str(auth))
    #Auth Şifreli Dosya ve doğrulaması

    #combine_File = sCrypt.combine_keys(maillist,auth, iv, key, mac_key, sCrypt.blocksize)
    #C:/Users/pc/Desktop/denemee_c.txt
    #ths = open("C:/Users/pc/Desktop/denemee_c.txt", "w")
    #ths.write(combine_File),
    #ths.close()
    combine_File=open('C:/Users/pc/Desktop/denemee_c.txt').read()
    #Auth(simetrikle şifreli)::::((mail::iv::key::mac_key::blocksize::+soldakilerin private şifreli halinin imzası).Bunun tamamı adamın publici ile şifreli):::():::()

    #imza=sCrypt.Asymmetric_Sign(combine_File,sCrypt.private_key)
    #sCrypt.Asymmetric_Auth(combine_File,imza,sCrypt.public_key)

    try:
        print("Sonuç:" + sCrypt.separate_File(combine_File))
    except:
        print("Hata !")

    #root.mainloop()


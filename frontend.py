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


TreeviewRootId=""
TreeviewReset=0
TreeviewRootIdDropbox=""
TreeviewResetDropbox=0
TreeviewRootIdFriendList=""
TreeviewResetFriendList=0

checklistlocal=[]
checklistfriends=[]
checklistDropbox=[]

app_key = "ph2b2jh4dqjxnew"
app_secret = "ixtrd7ua9h8hr3z"

# build the authorization URL:
authorization_url = "https://www.dropbox.com/oauth2/authorize?client_id=%s&response_type=code" % app_key
authorization_code=""
tokenid=""




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

    #onDoubleClick() fonksiyonunu ekleme
    #treeview.bind("<Double-Button-1>", onDoubleClick)

    listSubfolders(browsedDir)
    return (browsedDir)

def listSubfolders(path):

    dbx= dropbox.Dropbox(tokenid)

    treeview=t
    for p in os.listdir(path):
        sync = 0
        abspath = os.path.join(path, p)

        path = path.replace("\\", "/")
        abspath=abspath.replace("\\", "/")

        fileDropboxPath=abspath[19:]
        fullname = abspath

        try:
            if (os.path.isfile(fullname)):
                mtime = os.path.getmtime(fullname)
                mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                size = os.path.getsize(fullname)
                metadata = dbx.files_get_metadata(fileDropboxPath)
                print(mtime_dt)
                print(size)
                print(metadata.client_modified)
                print(metadata.size)
                if (mtime_dt == metadata.client_modified and size == metadata.size):
                    print("Senkron" + fileDropboxPath)

                    sync = 1
                else:
                    print("Senkron Değil:" + fileDropboxPath)

                    sync = 2

        except Exception as e:
            print(e)
            #print("Dosya Dropboxda Bulunmamaktadır 1 :" + fileDropboxPath)
            sync = 3

        if(treeview.exists(abspath)==False):
            treeview.insert(path, "end", abspath, text=p)

        if (sync == 1):
            treeview.sync1(fullname)
        if (sync == 2):
            treeview.sync2(fullname)
        if (sync == 3):
            treeview.sync3(fullname)

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

    treeview.insert('', 0, "Dropbox",text=browsedDir,open=True)

    #onDoubleClick() fonksiyonunu ekleme
    #treeview.bind("<Double-Button-1>", onDoubleClick)


    listSubfoldersDropbox("","Dropbox")
    return (browsedDir)

def listSubfoldersDropbox(path,parent):

    dbx= dropbox.Dropbox(tokenid)
    treeview=tdrop


    try:
        for p in dbx.files_list_folder(path).entries:
            sync = 0


            fullname="C:/Users/DropboxApp"+p.path_lower

            if (os.path.isfile(fullname)):
                try:
                    md = p.path_lower

                    mtime = os.path.getmtime(fullname)

                    mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])

                    size = os.path.getsize(fullname)

                    print("1")
                    print(p.path_lower)
                    metadata=dbx.files_get_metadata(p.path_lower)

                    print("2")

                    if(mtime_dt == metadata.client_modified and size == metadata.size):
                        #print("Senkron"+p.path_lower)
                        sync = 1
                    else:
                        #print("Senkron Değil:"+p.path_lower)
                        sync = 2

                except Exception as e:
                        #print(e)
                        #print("Dosya  Bulunmamaktadır 1 :" + p.path_lower)
                        sync=3


            treeview.insert(parent, 'end', p.path_lower, text=p.name, open=True)

            if (sync == 1):
                treeview.sync1(p.path_lower)
            if (sync == 2):
                treeview.sync2(p.path_lower)
            if (sync == 3):
                treeview.sync3(p.path_lower)


            listSubfoldersDropbox(p.path_lower,p.path_lower)

    except Exception as e:
        print()


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
        print(files[19:])
        print("Files: "+files)
        UploadFile(files,files[19:])
    for friends in checklistfriends:
        print("Friends: "+friends)

    ResetLocalDropbox()
    ResetDropbox()

def UploadFile(file_from,file_to):
    try:
        dbx=dropbox.Dropbox(tokenid)

        mtime = os.path.getmtime(file_from)
        print("Upload")
        print(mtime)
        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to,mode=dropbox.files.WriteMode.overwrite,client_modified=datetime.datetime(*time.gmtime(mtime)[:6]))

        writeConsoleMain(file_to+" Upload Successful")
        print(file_to + " Upload Successful")

    except Exception as e:
        writeConsoleMain(e)

def DownloadFile(file_from):
    dbx=dropbox.Dropbox(tokenid)
    file_to = "C:/Users/DropboxApp" + file_from  # + file_name[-1]                    dosya
    print(file_to)
    file_hierarchy_check = file_to.split('/')  # dosyaarray
    file_hierarchy_check.pop(0)  # for skipping the check for C: directory and Users
    file_hierarchy_check.pop(0)
    file_hierarchy_check.pop()  # skipping the check for the file that will be created
    current_folder = "C:/Users/"  # konum
    print(file_hierarchy_check)

    for file in file_hierarchy_check:
        print(file)
        file_to_create = current_folder + file
        print(file_to_create)
        if not os.path.exists(file_to_create):
            print("Creating folder according to your Dropbox file hierarchy")
            os.mkdir(file_to_create)
        else:
            print("Folder alredy exists")
        current_folder = file_to_create + "/"

    path_download = "C:/Users/DropboxApp" + file_from
    print(file_to)
    dbx.files_download_to_file(download_path=path_download, path=file_from)
    writeConsoleMain('Download successful '+file_to)
    print('Download successful '+file_to)


def callback(url):
    webbrowser.open_new(url)

def Login():
    global  authorization_code
    global tokenid
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
                time.sleep(1)
                login=1
        except:
                writeConsoleLogin("Hata access_token Bulunamadı")

    if (login==1):
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
UploadButton = tk.Button(MainFrame, text='Upload',command=UploadDropbox,relief='raised' ,borderwidth=5)

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

    LoginFrame = tk.Frame(root, width=1510, height=800, relief='raised', borderwidth=5)
    LoginFrame.pack()

    LoginPageButton = tk.Button(LoginFrame, text='Login', command=Login, relief='raised', borderwidth=5)
    LoginPageButton.place(x=130, y=120 ,width=100, height=25)

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
    global UploadButton

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
    UploadButton = tk.Button(MainFrame, text='Upload', command=UploadDropbox, relief='raised', borderwidth=5)
    UploadButton.place(x=10, y=350)


    Console = Text(MainFrame)
    Console.pack()
    Console['state'] = 'disabled'

    Console.place(x=850,y=10)

    #,command=MainToFriendFrame
    FriendPageButton = tk.Button(MainFrame, text='Add Friend',command=MainToFriendFrame,relief='raised' ,borderwidth=5)
    FriendPageButton.place(x=10,y=750)

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




def destroyFriendFrame():
    global FriendFrame
    FriendFrame.destroy()


if __name__ == '__main__':
    #os.utime(path_to_file, (access_time, modification_time))



    createLoginFrame()



    root.mainloop()


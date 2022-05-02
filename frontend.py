import tkinter as tk
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import ttk
from tkinter import *
from csv import writer
import pandas as pd
from tkinter import filedialog
import os
import emoji

TreeviewRootId=""
TreeviewReset=0
TreeviewRootIdDropbox=""
TreeviewResetDropbox=0
TreeviewRootIdFriendList=""
TreeviewResetFriendList=0









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

    def haschange(self,item):
        print(item)
        original_name=self.item(item,"text")
        if(original_name[0]!="🔴"):
            self.item(item, text="🔴 "+original_name)

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
            self.haschange(item)
            print("Tıklanan"+item)
            tags = self.item(item, "tags")
            if ("unchecked" in tags) or ("tristate" in tags):
                self.check_ancestor(item)
                self.check_descendant(item)
            else:
                self.uncheck_descendant(item)
                self.uncheck_ancestor(item)
            self.checkedList(TreeviewRootId)


    def checkedList(self,root):
        children = self.get_children(root)
        for item in children:
            tags = self.item(item, "tags")
            if("checked" in tags):
                print("checked"+item)
            self.checkedList(item)



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

    def haschange(self,item):
        print(item)
        original_name=self.item(item,"text")
        if(original_name[0]!="🔴"):
            self.item(item, text="🔴 "+original_name)

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
            self.haschange(item)
            print("Tıklanan"+item)
            tags = self.item(item, "tags")
            if ("unchecked" in tags) or ("tristate" in tags):
                self.check_ancestor(item)
                self.check_descendant(item)
            else:
                self.uncheck_descendant(item)
                self.uncheck_ancestor(item)
            self.checkedList(TreeviewRootIdFriendList)


    def checkedList(self,root):
        children = self.get_children(root)
        for item in children:
            tags = self.item(item, "tags")
            if("checked" in tags):
                print("checked"+item)
            self.checkedList(item)



class CheckboxTreeviewDropboxApp(ttk.Treeview):

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

    def haschange(self,item):
        print(item)
        original_name=self.item(item,"text")
        if(original_name[0]!="🔴"):
            self.item(item, text="🔴 "+original_name)

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
            self.haschange(item)
            print("Tıklanan"+item)
            tags = self.item(item, "tags")
            if ("unchecked" in tags) or ("tristate" in tags):
                self.check_ancestor(item)
                self.check_descendant(item)
            else:
                self.uncheck_descendant(item)
                self.uncheck_ancestor(item)
            self.checkedList(TreeviewRootIdDropbox)


    def checkedList(self,root):
        children = self.get_children(root)
        for item in children:
            tags = self.item(item, "tags")
            if("checked" in tags):
                print("checked"+item)
            self.checkedList(item)


def browseLocal():
    # clear the treeview before inserting new
    treeview=t
    for item in treeview.get_children():
        treeview.delete(item)

    #browsedDir = filedialog.askdirectory(initialdir="/", title="Select file")

    browsedDir="C:/Users/DropboxApp"
    treeview.insert('', 0, browsedDir,text=browsedDir,open=True)

    #onDoubleClick() fonksiyonunu ekleme
    #treeview.bind("<Double-Button-1>", onDoubleClick)

    listSubfolders(browsedDir)
    return (browsedDir)

def listSubfolders(path):
    treeview=t
    for p in os.listdir(path):
        abspath = os.path.join(path, p)

        path = path.replace("\\", "/")
        abspath=abspath.replace("\\", "/")

        #print("PARENT:"+path)
        #print("CHİLD:"+abspath)

        if(treeview.exists(abspath)==False):
            treeview.insert(path, "end", abspath, text=p)

        t.pack()

        if os.path.isdir(abspath):
            listSubfolders(abspath)

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

def writeConsole(*message, end = "\n", sep = " "):
    Console['state'] = 'normal'
    text = ""
    for item in message:
        text += "{}".format(item)
        text += sep
    text += end
    Console.insert(INSERT, text)
    Console['state'] = 'disabled'

def add_Friends():
    global FriendName
    global FriendMail
    global FriendPublicKey

    name=FriendName.get()
    mail = FriendMail.get()
    publickey = FriendPublicKey.get()
    print(name)
    list_data=[name,mail,publickey]
    with open('friendlist.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list_data)
        f_object.close()

def read_Friends():
    data=pd.read_csv("friendlist.csv")
    print( data.head())
    data.info()

    y=data["totalDuration"]
    x=data.drop("totalDuration",axis=1)

def MainToFriendFrame():
    destroyMainFrame()
    createFriendFrame()

def FriendToMainFrame():
    destroyFriendFrame()
    createMainFrame()


root = tk.Tk()
root.title('DropboxApp')
root.geometry('1510x800')
LoginFrame=tk.Frame()
MainFrame= tk.Frame(root, width=1510, height=800, relief='raised', borderwidth=5)
FriendFrame=tk.Frame()



treeviewLocal= ttk.Treeview(MainFrame)
t=CheckboxTreeviewLocalApp(treeviewLocal,height=20)
FriendListTreeview = ttk.Treeview(MainFrame)
fl = CheckboxFriendList(FriendListTreeview, height=20)
Console = Text(MainFrame)
FriendPageButton = tk.Button(MainFrame, text='Hello',command=MainToFriendFrame,relief='raised' ,borderwidth=5)

MainPageButton = tk.Button(FriendFrame, text='Main Page', command=FriendToMainFrame, relief='raised',borderwidth=5)
FriendName = tk.Entry(FriendFrame)
FriendMail = tk.Entry(FriendFrame)
FriendPublicKey = tk.Entry(FriendFrame)

def createMainFrame():
    global root
    global MainFrame
    global treeviewLocal
    global t
    global FriendListTreeview
    global fl
    global Console
    global FriendPageButton


    MainFrame = tk.Frame(root, width=1510, height=800, relief='raised', borderwidth=5)
    MainFrame.pack()




    treeviewLocal = ttk.Treeview(MainFrame)
    treeviewLocal.place(x=10, y=10, width=410)
    t=CheckboxTreeviewLocalApp(treeviewLocal,height=20)
    t.pack()

    FriendListTreeview = ttk.Treeview(MainFrame)
    FriendListTreeview.place(x=430, y=10, width=410)
    fl = CheckboxFriendList(FriendListTreeview, height=20)
    fl.pack()


    browseLocal()
    Console = Text(MainFrame)
    Console.pack()
    Console['state'] = 'disabled'

    Console.place(x=850,y=10)

    #,command=MainToFriendFrame
    FriendPageButton = tk.Button(MainFrame, text='Add Friend',command=MainToFriendFrame,relief='raised' ,borderwidth=5)
    FriendPageButton.place(x=10,y=750)








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




def destroyFriendFrame():
    global FriendFrame
    FriendFrame.destroy()


if __name__ == '__main__':





    createFriendFrame()





    root.mainloop()


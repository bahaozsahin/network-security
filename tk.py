import tkinter as tk
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import ttk

from tkinter import filedialog
import os

TreeviewRootId=""
TreeviewReset=0



class CheckboxTreeview(ttk.Treeview):
    """
        Treeview widget with checkboxes left of each item.
        The checkboxes are done via the image attribute of the item, so to keep
        the checkbox, you cannot add an image to the item.
    """


    def __init__(self, master=None, **kw):
        ttk.Treeview.__init__(self, master, **kw)
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



def browse():
    # clear the treeview before inserting new
    treeview=t
    for item in treeview.get_children():
        treeview.delete(item)

    browsedDir = filedialog.askdirectory(initialdir="/", title="Select file")
    treeview.insert('', 0, browsedDir,text=browsedDir)

    treeview.bind("<Double-Button-1>", onDoubleClick)

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

def obey_ancestor(iid):
    """
    If the status of an item is toggled, the status of all its descendants
    is also set to the new status.
    """
    set_status = t.uncheck if t.checked(iid) else t.check
    stack = [iid]
    while stack:
        iid = stack.pop()
        set_status(iid)
        stack.extend(t.get_children(iid))

    print(t.pack())


if __name__ == '__main__':
    root = tk.Tk()
    t = CheckboxTreeview(root, show="tree")
    t.pack()
    #t.insert("", 0, "1", text="1")
    #t.insert("1", "end", "11", text="1")
    #t.insert("1", "end", "12", text="2")
    browse()
    root.mainloop()


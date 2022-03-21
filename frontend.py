from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
from turtle import title


##########################Login
scrLogin = Tk()
scrLogin.title('Kullanıcı Girişi')
scrLogin.geometry('750x800')
scrLogin.config(bg="#447c84")

def validateLogin():
    scrLogin.destroy()


# frame
frame = Frame(scrLogin, padx=20, pady=20)
frame.pack(expand=True)
# frame.pack_propagate(False)
# frame.pack(expand=True)

# labels
lblUser = Label(frame, text='Kullanıcı Adı: ', font='Times 14 bold').grid(row=3, column=0, pady=5)

lblPwd = Label(frame, text='Şifre: ', font='Times 14 bold').grid(row=4, column=0, pady=5)

# Entry
entUser = Entry(frame, width=20)
entPwd = Entry(frame, width=20, show="*")
entUser.grid(row=3, column=1)
entPwd.grid(row=4, column=1)

# button
btnLogin = Button(frame, text='Giriş', font='Times 14 bold', padx=20, pady=10, command=validateLogin)
btnLogin.grid(row=6, column=0, pady=20)

scrLogin.mainloop()


##########################Logged

def listSubfolders(path, parent):

    for p in os.listdir(path):
        abspath = os.path.join(path, p)
        parent_element = treeview.insert(parent, 'end', text=p, open=True)
        if os.path.isdir(abspath):
            listSubfolders(abspath, parent_element)
    print('listsubfolder sonu')


def browse(root):
    """
    root = Tk()
    root.filename = filedialog.askdirectory(initialdir="/", title= "Select file")
    root.destroy()"""
    browsedDir = filedialog.askdirectory(initialdir="/", title = "Select file")
    treeview.insert('', 0, text = browsedDir, open=True)
    
    listSubfolders(browsedDir, root)
    #global browsedDirectory 
    #browsedDirectory = browsedDir
    return(browsedDir)
    #return (root.filename)

scrLogged = Tk()
scrLogged.title('Dosya Gezgini')
scrLogged.geometry('750x800')
scrLogged.config(bg="#447c84")


treeview = ttk.Treeview(scrLogged)
treeview.heading("#0" ,text="Directory")
root = treeview.insert('', 'end', open=True)

btnBrowse = Button(scrLogged, text='Browse', font='Times 14 bold', padx=20, pady=40, command=lambda: browse(root)).pack()




# frames
#frame = Frame(ws, padx=20, pady=20)
#frame.pack(expand=True)

#lblFile = ttk.Label(frame, text='Dosya Dizini').pack()
script_directory = os.path.dirname(os.path.abspath(__file__))
# Now, let's build our file/folder list
dir_contents = []
for subdir, dirs, files in os.walk(script_directory):
    dir_contents = [subdir, dirs, files]
    break


treeview.pack()

scrLogged.mainloop()

from asyncio.windows_events import NULL
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os


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
    print(path)

    for p in os.listdir(path):
        if p == '' or p == NULL or p == "C:/Users/bahao/network/DropboxIO":
            p = path

        abspath = os.path.join(path, p)
        
        parent_element = treeview.insert(parent, 'end', text=p, open=True)
        if os.path.isdir(abspath):
            listSubfolders(abspath, parent_element)
   


def browse():
    #clear the treeview before inserting new
    for item in treeview.get_children():
        treeview.delete(item)


    browsedDir = filedialog.askdirectory(initialdir="/", title = "Select file")
    root = treeview.insert('', 0, text = browsedDir, open=True)
    
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
#root = treeview.insert('', 'end', open=True)

btnBrowse = Button(scrLogged, text='Browse', font='Times 14 bold', padx=20, pady=40, command= browse).pack()




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

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import stat
import dropbox
import unicodedata
import datetime
import time
import six
import contextlib

authToken = "sl.BEO7w2ExtNwHTEruPlDysQRPacA9poeu5BWPOJ-z8thqW_E5E3JrSPSEc1-k2pS3z0tiJTNj33MFqpxi-WsxAmVfZ3ck4Q7F3eEX3EEdqKMWDKJpY57fWBtwsQoK05aekfBbnTOk"
# connect
dbx = dropbox.Dropbox(authToken)


def main():
    default_path = 'C:/Users/bahao/network/dbxio/'
    null_path = ""
    example_path = "/Deneme"
    file_from = 'deneme.txt'
    file_to = '/Deneme/uploadTest.txt'
    file_path = '/Deneme/downloadTest.txt'

    localDir = 'C:/Users/bahao/network/DropboxIO/'

    if not os.path.exists(localDir):
        print(localDir, 'does not exist on your filesystem')

    dbxDir = 'Deneme'

    print("denemedeneme")
    print(localDir)

    # for entry in dbx.files_list_folder('').entries:
    # print(entry.name)

    for dn, dirs, files in os.walk(localDir):

        subfolder = dn[len(localDir):].strip(os.path.sep)
        listing = list_folder(dbx, dbxDir, subfolder)
        print('Descending into', subfolder, '...')

        # First do all the files.
        for name in files:
            fullname = os.path.join(dn, name)
            if not isinstance(name, six.text_type):
                name = name.decode('utf-8')
            nname = unicodedata.normalize('NFC', name)
            if name.startswith('.'):
                print('Skipping dot file:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary file:', name)
            elif name.endswith('.pyc') or name.endswith('.pyo'):
                print('Skipping generated file:', name)
            elif nname in listing:
                md = listing[nname]
                mtime = os.path.getmtime(fullname)
                mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                size = os.path.getsize(fullname)
                if (isinstance(md, dropbox.files.FileMetadata) and
                        mtime_dt == md.client_modified and size == md.size):
                    print(name, 'is already synced [stats match]')
                else:
                    print(name, 'exists with different stats, downloading')
                    res = download(dbx, dbxDir, subfolder, name)
                    with open(fullname) as f:
                        data = f.read()
                    if res == data:
                        print(name, 'is already synced [content match]')
                    else:
                        print(name, 'has changed since last sync')
                        # if yesno('Refresh %s' % name, False, args):
                        upload(dbx, fullname, dbxDir, subfolder, name,
                               overwrite=True)
            # elif yesno('Upload %s' % name, True, args):
            upload(dbx, fullname, dbxDir, subfolder, name)

        # Then choose which subdirectories to traverse.
        keep = []
        for name in dirs:
            if name.startswith('.'):
                print('Skipping dot directory:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary directory:', name)
            elif name == '__pycache__':
                print('Skipping generated directory:', name)
            # elif yesno('Descend into %s' % name, True, args):
            print('Keeping directory:', name)
            keep.append(name)
            # else:
            #    print('OK, skipping directory:', name)
        dirs[:] = keep

    dbx.close()


def list_folder(dbx, folder, subfolder):
    """
    List a folder.
    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
    path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
    while '//' in path:
        path = path.replace('//', '/')
    path = path.rstrip('/')
    try:
        with stopwatch('list_folder'):
            res = dbx.files_list_folder(path)

    except dropbox.exceptions.ApiError as err:
        print('Folder listing failed for', path, '-- assumed empty:', err)
        return {}
    else:
        rv = {}
        for entry in res.entries:
            rv[entry.name] = entry
        return rv


def download(dbx, folder, subfolder, name):
    """Download a file.
    Return the bytes of the file, or None if it doesn't exist.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    with stopwatch('download'):
        try:
            md, res = dbx.files_download(path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
    data = res.content
    print(len(data), 'bytes; md:', md)
    return data


def upload(dbx, fullname, folder, subfolder, name, overwrite=False):
    """Upload a file.
    Return the request response, or None in case of error.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    mtime = os.path.getmtime(fullname)
    with open(fullname, 'rb') as f:
        data = f.read()
    with stopwatch('upload %d bytes' % len(data)):
        try:
            res = dbx.files_upload(
                data, path, mode,
                client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                mute=True)
        except dropbox.exceptions.ApiError as err:
            print('*** API error', err)
            return None
    print('uploaded as', res.name.encode('utf8'))
    return res


@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))


main()

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
        # if p == '' or p == NULL or p == "C:/Users/bahao/network/DropboxIO":
        #    p = path

        abspath = os.path.join(path, p)
        # print("Path1:"+path)
        path = path.replace("\\", "/")
        # print("Path2:"+path)
        parent_element = treeview.insert(parent, 'end', text=p, values=path, open=True)

        if os.path.isdir(abspath):
            listSubfolders(abspath, parent_element)


def listSubfoldersDropbox(oncekipath, parent):
    try:
        for p in dbx.files_list_folder(oncekipath).entries:
            oncekipath = p.path_lower
            parent_element = treeview2.insert(parent, 'end', text=p.name, values=oncekipath, open=True)
            listSubfoldersDropbox(oncekipath, parent_element)

    except:
        print("Alt Dosyasi Yok")


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


def onDoubleClickDropbox(event):
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
        print("")
    else:
        newpath = item['text']
    print(newpath)
    global pathForDownload
    pathForDownload = newpath


def browse():
    # clear the treeview before inserting new
    for item in treeview.get_children():
        treeview.delete(item)

    browsedDir = filedialog.askdirectory(initialdir="/", title="Select file")
    root = treeview.insert('', 0, text=browsedDir, open=True)
    treeview.bind("<Double-Button-1>", onDoubleClick)

    listSubfolders(browsedDir, root)
    # global browsedDirectory
    # browsedDirectory = browsedDir
    return (browsedDir)
    # return (root.filename)


def otoDropbox():
    root = treeview2.insert('', 0, text='Dropbox', open=True)
    treeview2.bind("<Double-Button-1>", onDoubleClickDropbox)
    listSubfoldersDropbox("", root)


def uploadSelected(file_from):
    file_name = file_from.split("/")
    file_to = "/Uploads/" + file_name[-1]
    with open(file_from, 'rb') as f:
        dbx.files_upload(f.read(), file_to)

    print("Upload successful")


def downloadSelected(file_from):
    file_to = "C:/Users/DropboxDownloads" + file_from # + file_name[-1]                    dosya
    print(file_to)
    file_hierarchy_check = file_to.split('/')                                               #dosyaarray
    file_hierarchy_check.pop(0) #for skipping the check for C: directory and Users
    file_hierarchy_check.pop(0)
    file_hierarchy_check.pop() #skipping the check for the file that will be created
    current_folder = "C:/Users/"                                                            #konum
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
    
    path_download = "C:/Users/DropboxDownloads" + file_from
    print(file_to)
    dbx.files_download_to_file(download_path= path_download , path = file_from)

    #data = res.content
    #print(len(data), 'bytes; md:', md)
    print('Download successful')


scrLogged = Tk()
scrLogged.title('Dosya Gezgini')
scrLogged.geometry('750x800')
scrLogged.config(bg="#447c84")

treeview = ttk.Treeview(scrLogged)
treeview.heading("#0", text="Directory")
treeview.place(x=10, y=150, width=400)
btnUpload = Button(scrLogged, text='Upload', font='Times 18 bold', command=lambda: uploadSelected(pathForUpload))
btnUpload.place(x=450, y=330)

treeview2 = ttk.Treeview(scrLogged)
treeview2.heading("#0", text="Directory2")
treeview2.place(x=10, y=400, width=400)
btnDownload = Button(scrLogged, text='Download', font='Times 18 bold', command=lambda: downloadSelected(pathForDownload))
btnDownload.place(x=450, y=580)

otoDropbox()

# root = treeview.insert('', 'end', open=True)

btnBrowse = Button(scrLogged, text='Browse', font='Times 14 bold', padx=20, pady=40, command=browse).pack()

# frames
# frame = Frame(ws, padx=20, pady=20)
# frame.pack(expand=True)

# lblFile = ttk.Label(frame, text='Dosya Dizini').pack()
script_directory = os.path.dirname(os.path.abspath(__file__))
# Now, let's build our file/folder list
dir_contents = []
for subdir, dirs, files in os.walk(script_directory):
    dir_contents = [subdir, dirs, files]
    break

# treeview.pack()

scrLogged.mainloop()

#from Tkinter import *
def create_menu(root):
    menu = tk.Menu(root)
    root.config(menu=menu)
    # menu 1
    filemenu = tk.Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New")
    filemenu.add_command(label="Open...", command=addmodel)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    # menu 2

    cammenu = tk.Menu(menu)
    menu.add_cascade(label="Camera",menu=cammenu)
    cammenu.add_command(label="Start Camera")
    cammenu.add_command(label="Stop Camera")
    cammenu.add_separator()
    cammenu.add_command(label="Capture Image",command=capturef)



def quit_(root):
    root.destroy()

import tkinter as tk

# TODO we could probably abstract this further and separate menus into their own
# files


class MainMenu:
    def __init__(self, master):
        self.master = master
        master.title("Hello World")


root = tk.Tk()
my_gui = MainMenu(root)
root.mainloop()

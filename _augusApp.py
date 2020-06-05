# from tkinter import *
from tkinter import ttk, Tk, Menu
from PyQt5 import QtCore, QtGui, QtWidgets

class AugusApp():
    def __init__(self):
        self.buildGUI()

    def buildGUI(self):
        self.root = Tk()
        self.root.geometry('800x600')
        self.root.title("Augus - 0.1")
        self.root.resizable(1,1)
        self.root.iconbitmap('augus.ico')
        self.root.configure(bg = 'white')

        # Menubar
        self.menubar = Menu(self.root)
        self.root.config(menu = self.menubar)

        self.filemenu = Menu(self.root, tearoff = 0)
        self.editmenu = Menu(self.root, tearoff = 0)
        self.runmenu = Menu(self.root, tearoff = 0)
        self.toolmenu = Menu(self.root, tearoff = 0)
        self.helpmenu = Menu(self.root, tearoff = 0)

        self.menubar.add_cascade(label = "File", menu = self.filemenu, underline = 0)
        self.menubar.add_cascade(label = "Edit", menu = self.editmenu, underline = 0)
        self.menubar.add_cascade(label = "Run", menu = self.runmenu, underline = 0)
        self.menubar.add_cascade(label = "Tools", menu = self.toolmenu, underline = 0)
        self.menubar.add_cascade(label = "Help", menu = self.helpmenu, underline = 0)

        self.filemenu.add_command(label = "New", underline = 0, accelerator = "Ctrl+N")
        self.filemenu.add_command(label = "Open", underline = 0, accelerator = "Ctrl+O")
        self.filemenu.add_separator()
        self.filemenu.add_command(label = "Save", underline = 0, accelerator = "Ctrl+S")
        self.filemenu.add_command(label = "Save As", underline = 5, accelerator = "Ctrl+Shift+S")
        self.filemenu.add_separator()
        self.filemenu.add_command(label = "Exit", underline = 1, command = self.root.quit)
       
        self.editmenu.add_command(label = "Undo",  underline = 0, accelerator = "Ctrl+Z")
        self.editmenu.add_command(label = "Redo",  underline = 0, accelerator = "Ctrl+Y")
        self.editmenu.add_separator()
        self.editmenu.add_command(label = "Cut",  underline = 2, accelerator = "Ctrl+X")
        self.editmenu.add_command(label = "Copy", underline = 0, accelerator = "Ctrl+C")
        self.editmenu.add_command(label = "Paste", underline = 0, accelerator = "Ctrl+V")
        self.editmenu.add_separator()
        self.editmenu.add_command(label = "Find", underline = 0, accelerator = "Ctrl+F")
        self.editmenu.add_command(label = "Replace", underline = 0, accelerator = "Ctrl+H")
        
        self.runmenu.add_command(label = "Ascendent Debugging", underline = 0, accelerator = "F5")
        self.runmenu.add_command(label = "Ascendent Without Debugging", underline = 0, accelerator = "Ctrl+F5")
        self.runmenu.add_command(label = "Descendent Without Debugging", underline = 0, accelerator = "Ctrl+Alt+F5")
        self.runmenu.add_separator()
        self.runmenu.add_command(label = "Restart Debugging", state = "disabled",  underline = 0, accelerator = "Ctrl+Shift+F5")
        self.runmenu.add_command(label = "Stop Debugging", state = "disabled", underline = 0, accelerator = "Shift+F5")
        self.runmenu.add_command(label = "Step Into", state = "disabled",  underline = 0, accelerator = "F11")
        self.runmenu.add_command(label = "Continue", state = "disabled",  underline = 0, accelerator = "F6")

        self.toolmenu.add_checkbutton(label = "Dark Mode",  underline = 0)

        self.helpmenu.add_command(label = "About",  underline = 0)

        # TabControl
        self.tabcontrol = ttk.Notebook(self.root)
        tab1 = ttk.Frame(self.tabcontrol)
        tab2 = ttk.Frame(self.tabcontrol)
        self.tabcontrol.add(tab1, text = 'Tab 1')
        self.tabcontrol.add(tab2, text = 'Tab 2')
        self.tabcontrol.pack(expand = 1, fill = "both")

        self.root.bind_all("<Control-N>", self.deleteSelectedTab)
        self.root.bind_all("<Control-O>", self.deleteSelectedTab)
        self.root.bind_all("<Control-S>", self.deleteSelectedTab)
        self.root.bind_all("<Control-Shift-S>", self.deleteSelectedTab)
        self.root.bind_all("<Control-Alt-S>", self.deleteSelectedTab)
        self.root.bind_all("<Control-F4>", self.deleteSelectedTab)
        self.root.bind_all("<Control-W>", self.deleteSelectedTab)
        self.root.bind_all("<Control-Z>", self.deleteSelectedTab)
        self.root.bind_all("<Control-Y>", self.deleteSelectedTab)
        self.root.bind_all("<Control-F>", self.deleteSelectedTab)
        self.root.bind_all("<Control-H>", self.deleteSelectedTab)
        self.root.bind_all("<F5>", self.deleteSelectedTab)
        self.root.bind_all("<Control-F5>", self.deleteSelectedTab)
        self.root.bind_all("<Control-Alt-F5>", self.deleteSelectedTab)

        self.root.bind_all("<Control-Shift-F5>", self.deleteSelectedTab)
        self.root.bind_all("<Shift-F5>", self.deleteSelectedTab)
        self.root.bind_all("<F11>", self.deleteSelectedTab)
        self.root.bind_all("<F6>", self.deleteSelectedTab)

        self.root.mainloop()


    def deleteSelectedTab(self, event=None):
        for item in self.tabcontrol.winfo_children():
            if str(item) == self.tabcontrol.select():
                item.destroy()
                return


def main():
    AugusApp()
    return 0

if __name__ == '__main__':
    main()
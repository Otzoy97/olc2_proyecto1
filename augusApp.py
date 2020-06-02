# from tkinter import *
from tkinter import ttk, Tk
class AugusApp():
    def __init__(self):
        self.root = Tk()
        self.root.title("Augus - 0.1")
        self.root.resizable(1,1)
        self.root.iconbitmap('augus.ico')
        self.root.mainloop()

def main():
    AugusApp()
    return 0

if __name__ == '__main__':
    main()
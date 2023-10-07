from tkinter import *
from frame import Window

try:
    root = Tk()
    win = Window(root)
    root.mainloop()

except ImportError:
    print('Dependencies not found, installing...')
    import subprocess

    subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
    print("Dependencies installed successfully.")

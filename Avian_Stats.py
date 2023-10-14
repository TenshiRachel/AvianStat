from tkinter import *


def main():
    try:
        from frame import Window

        root = Tk()
        win = Window(root)
        root.mainloop()

    except ModuleNotFoundError:
        # If user does not have dependencies, auto install
        print('Dependencies not found, installing...')
        print('This takes about a minute, please wait')
        import subprocess

        subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully.")
        # Run app again after installing
        main()


if __name__ == '__main__':
    main()

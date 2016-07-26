import Tkinter as Tk
import MainMenu


def main():
    root = Tk.Tk()
   # root.geometry("1024x768")

    root.attributes('-fullscreen', True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

    root.configure(bg="white")
    root.update()
    MainMenu.MainMenu(root)
    root.mainloop()

if __name__ == '__main__':
    main()

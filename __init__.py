import Tkinter as Tk
import App

root = Tk.Tk()
# w, h = root.winfo_screenwidth(), root.winfo_screenheight()
# root.geometry("%dx%d+0+0" % (w, h))
root.geometry("1024x768")

# root.overrideredirect(True)
# root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

root.configure(bg="white")
root.update()

app = App.App(root)

root.mainloop()
# root.destroy() # optional; see description below

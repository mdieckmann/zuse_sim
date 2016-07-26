import Tkinter as Tk
import App

class MainMenu(object):
    def __init__(self, master):
        self.master = master
        self.width = master.winfo_width()
        self.height = master.winfo_height()
        f_text = Tk.Frame(master, bg = 'white', width = self.width, height = self.height / 6,bd=1)
        f_text.grid(row = 0, column = 0, columnspan = 2)
        f_text.grid_propagate(False)
        f_instruction = Tk.Frame(master, bg = 'white', width = self.width, height = self.height / 6,bd=1)
        f_instruction.grid(row = 1, column = 0, columnspan = 2)
        f_instruction.grid_propagate(False)
        fleft = Tk.Frame(master, bg = 'white', width = self.width / 2, height = self.height * 2 / 3)
        fleft.grid(row = 2, column = 0)
        fright = Tk.Frame(master, bg = 'white', width = self.width / 2, height = self.height * 2 / 3)
        fright.grid(row = 2, column = 1)

        header = Tk.Label(f_text, text='Simulation of Konrad Zuses "logistische Maschine"', font = "Helvetica 16 bold",bg = 'white')
        header.place(relx=0.5, rely=0.5, anchor=Tk.CENTER)
        instruction = Tk.Label(f_instruction, text='Use the Buttons to select a Program',font = "Helvetica 12",bg = 'white')
        instruction.place(relx=0.5, rely=0.2, anchor=Tk.CENTER)

        fl1 = Tk.Frame(fleft,width = self.width / 2, height = self.height * 2 / 9)
        fl1.pack_propagate(0)
        fl1.pack()
        fl2 = Tk.Frame(fleft,width = self.width / 2, height = self.height * 2 / 9)
        fl2.pack_propagate(0)
        fl2.pack()
        fl3 = Tk.Frame(fleft,width = self.width / 2, height = self.height * 2 / 9)
        fl3.pack_propagate(0)
        fl3.pack()
        button1 = Tk.Button(fl1,text = 'QUIT', command = self.close_window, bg = 'white')
        button1.pack(fill=Tk.BOTH,expand = 1)
        button2 = Tk.Button(fl2,text = 'Addition of 2 4-Bit Integers \n~5 minutes', command = self.add_4_bit,bg = 'white')
        button2.pack(fill=Tk.BOTH,expand = 1)
        button3 = Tk.Button(fl3,text = 'Addition of 2 8-Bit Integers \n~10 minutes', command = self.add_8_bit,bg = 'white')
        button3.pack(fill=Tk.BOTH,expand = 1)

        fr1 = Tk.Frame(fright,width = self.width / 2, height = self.height * 2 / 9)
        fr1.pack_propagate(0)
        fr1.pack()
        fr2 = Tk.Frame(fright,width = self.width / 2, height = self.height * 2 / 9)
        fr2.pack_propagate(0)
        fr2.pack()
        fr3 = Tk.Frame(fright,width = self.width / 2, height = self.height * 2 / 9)
        fr3.pack_propagate(0)
        fr3.pack()
        button4 = Tk.Button(fr1,text = 'Subtraction of 2 4-Bit Integers. \n~10 minutes', command = self.sub_4_bit,bg = 'white')
        button4.pack(fill=Tk.BOTH,expand = 1)
        button5 = Tk.Button(fr2,text = 'Multiplication of 2 3-Bit Integers. \n~17 minutes', command = self.mul_3_bit, bg = 'white')
        button5.pack(fill=Tk.BOTH,expand = 1)
        button6 = Tk.Button(fr3,text = 'Division of 2 3-Bit Integers \n~50(!) minutes', command = self.div_3_bit,bg = 'white')
        button6.pack(fill=Tk.BOTH,expand = 1)

    def add_4_bit(self):
        self.new_window('add_4_bit.txt','Adding Numbers t0-t3 and t4-t7.', 't10-t14',5)

    def add_8_bit(self):
        self.new_window('add_8_bit.txt','Adding Numbers t0-t7 and t10-t17','t18-t26',10)

    def sub_4_bit(self):
        self.new_window('sub_4_bit.txt','Subtracting Number t4-t7 from t0-t3.', 't11-t15.',10)

    def mul_3_bit(self):
        self.new_window('mul_3_bit.txt','Multiplying Numbers t0-t2 and t3-t5.', 't20-t25',17)

    def div_3_bit(self):
        self.new_window('div_3_bit.txt','Dividing Number t0-t2 by t3-t5.','t18-t20 with remainder t27-t32.',50)

    def new_window(self,file_name,input_info,output_info,duration_estimate):
        self.newWindow = Tk.Toplevel(self.master)

        self.newWindow.attributes('-fullscreen', True)
        self.newWindow.geometry("{0}x{1}+0+0".format(self.newWindow.winfo_screenwidth(), self.newWindow.winfo_screenheight()))

        #self.newWindow.geometry("1024x768")
        self.newWindow.configure(bg="white")

        self.newWindow.update()
        self.app = App.App(self.newWindow,file_name,input_info,output_info,duration_estimate)
    def close_window(self):
        self.master.destroy()

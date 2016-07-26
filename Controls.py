import Tkinter as Tk
from datetime import datetime,timedelta


class Controls(object):
    def __init__(self, master, width, height,app,input_info,duration_estimate):
        self.master = master
        self.input_info = input_info
        self.duration_estimate = duration_estimate
        self.app = app
        self.height = height * 1 / 17
        self.width = width * 14 / 18

        text_frame = Tk.Frame(master,bg = 'white',width = self.width * 6 / 14, height = self.height)
        text_frame.grid(row=1, column = 3, rowspan = 1, columnspan = 6)
        text_frame.grid_propagate(False)

        start_button_frame = Tk.Frame(master,bg = 'white',width = self.width * 4 / 14, height = self.height)
        start_button_frame.grid(row=1, column = 9, rowspan = 1, columnspan = 4)
        quit_button_frame = Tk.Frame(master,bg = 'white',width = self.width * 4 / 14, height = self.height)
        quit_button_frame.grid(row=1, column = 13, rowspan = 1, columnspan = 4)

        quit_btn_hlp = Tk.Frame(start_button_frame,bg = 'white',width = self.width * 4 / 14, height = self.height)
        quit_btn_hlp.pack_propagate(0)
        quit_btn_hlp.pack()
        start_btn_hlp = Tk.Frame(quit_button_frame,bg = 'white',width = self.width * 4 / 14, height = self.height)
        start_btn_hlp.pack_propagate(0)
        start_btn_hlp.pack()

        self.info_text = Tk.Label(text_frame, text='Click the memory cells to flip their bit. Use the mouse wheel to scroll the memory.\n' + self.input_info, bg = 'white',wraplength=self.width * 5 / 14)
        self.info_text.place(relx=0.5, rely=0.5, anchor=Tk.CENTER)
        quit_button = Tk.Button(quit_btn_hlp,bg = 'white',text = 'QUIT', command = self.close_windows)
        quit_button.pack(fill=Tk.BOTH,expand = 1)
        self.start_button = Tk.Button(start_btn_hlp,bg = 'white',text = 'START', command = self.start_animation)
        self.start_button.pack(fill=Tk.BOTH,expand = 1)

    def close_windows(self):

        if self.app.cable.switch_done.get() == 0:
            self.app.cable.switch_done.set(1)

        if self.app.cable.flow_done.get() == 0:
            self.app.cable.flow_done.set(1)

        if self.app.memory.done.get() == 0:
            self.app.memory.done.set(1)

        if self.app.memory.color_blink_done.get() == 0:
            self.app.memory.color_blink_done.set(1)

        if self.app.memory_op.color_blink_done.get() == 0:
            self.app.memory_op.color_blink_done.set(1)

        if self.app.memory_op.switch_done.get() == 0:
            self.app.memory_op.switch_done.set(1)

        if self.app.memory_op.flow_done.get() == 0:
            self.app.memory_op.flow_done.set(1)

        if self.app.processor.switch_done.get() == 0:
            self.app.processor.switch_done.set(1)

        if self.app.processor.flow_done.get() == 0:
            self.app.processor.flow_done.set(1)

        if self.app.register.flow_done.get() == 0:
            self.app.register.flow_done.set(1)

        if self.app.register.color_blink_done.get() == 0:
            self.app.register.color_blink_done.set(1)

        if self.app.register.flag_move_done.get() == 0:
            self.app.register.flag_move_done.set(1)

        if self.app.register.flag_toggle_done.get() == 0:
            self.app.register.flag_toggle_done.set(1)

        if self.app.wheel.wheel_done.get() == 0:
            self.app.wheel.wheel_done.set(1)

        if self.app.wheel.flow_done.get() == 0:
            self.app.wheel.flow_done.set(1)

        self.master.destroy()

    def start_animation(self):
        print 'START'
        now_plus = datetime.now() + timedelta(minutes = self.duration_estimate)
        now_plus = datetime.strftime(now_plus, '%H:%M')
        input_info = self.input_info + '\n ETA ~' + now_plus
        self.info_text.configure(text=input_info)
        self.app.memory.init_additional_memory()
        self.start_button.configure(state=Tk.DISABLED)
        self.app.run_app()
import Tkinter as Tk
import Wheel
import Register
import Out
import Cable
import Processor
import Memory
import MemoryOp

class App(object):
    def __init__(self, master):
        self.root = master
        self.canvas_width = master.winfo_width()
        self.canvas_height = master.winfo_height()
        arrow_width = self.canvas_height / 200
        border = 0

        #processor must be initialized first
        processor = Processor.Processor(master,self.canvas_width,self.canvas_height,arrow_width,border)
        wheel = Wheel.Wheel(master,self.canvas_width,self.canvas_height,border,arrow_width)
        register = Register.Register(master,self.canvas_width,self.canvas_height,border,processor.exit_height,arrow_width)
        out = Out.Out(master,self.canvas_width,self.canvas_height,border)
        memory = Memory.Memory(master,self.canvas_width,self.canvas_height,border)
        memory_op = MemoryOp.MemoryOp(master,self.canvas_width,self.canvas_height,arrow_width,border)
        cable = Cable.Cable(master,self.canvas_width,self.canvas_height,arrow_width,border,processor.entry_width,memory_op.entry_width,wheel.exit_height)

        for i in range(2):
            wheel.next_command()
        target = [1,1,1,0,1,1,0]
        processor.set_switch(target)
        master.wait_variable(processor.switch_done)
        wheel.set_flow('red')
        cable.set_flow('red')
        processor.set_flow('red')
        register.set_flow('red')
        register.set_register('A',1)
        wheel.set_flow('black')
        cable.set_flow('black')
        processor.set_flow('black')
        register.set_flow('black')

        for i in range(2):
            wheel.next_command()
        cable.set_switch(1)
        master.wait_variable(cable.switch_done)
        wheel.set_flow('red')
        cable.set_flow('red')
        memory_op.set_flow('red')
        memory_op.toggle_blink()
        memory.set_target(6)
        register.set_register('A',0)
        wheel.set_flow('black')
        cable.set_flow('black')
        memory_op.set_flow('black')

        master.destroy()

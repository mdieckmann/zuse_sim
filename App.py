import Tkinter as Tk
import Wheel
import Register
import OutTop
import OutBottom
import OutLeft
import OutRight
import Cable
import Processor
import Memory
import MemoryOp
import time
import sys
import re

class App(object):

    def __init__(self, master):
        self.master = master
        border_width = 15
        self.canvas_width = master.winfo_width()
        self.canvas_height = master.winfo_height()
        arrow_width = self.canvas_height / 200
        border = 0

        #processor must be initialized first
        OutTop.OutTop(master, self.canvas_width, self.canvas_height, border,border_width)
        OutBottom.OutBottom(master, self.canvas_width, self.canvas_height, border,border_width)
        OutLeft.OutLeft(master, self.canvas_width, self.canvas_height, border,border_width)
        OutRight.OutRight(master, self.canvas_width, self.canvas_height, border,border_width)
        self.processor = Processor.Processor(master,self.canvas_width,self.canvas_height,arrow_width,border)
        self.wheel = Wheel.Wheel(master,self.canvas_width,self.canvas_height,border,arrow_width)
        self.register = Register.Register(master,self.canvas_width,self.canvas_height,border,self.processor.exit_height,arrow_width)
        self.memory = Memory.Memory(master,self.canvas_width,self.canvas_height,border)
        self.memory_op = MemoryOp.MemoryOp(master,self.canvas_width,self.canvas_height,arrow_width,border)
        self.cable = Cable.Cable(master,self.canvas_width,self.canvas_height,arrow_width,border,self.processor.entry_width,self.memory_op.entry_width,self.wheel.exit_height)

## TODO : MEANINGFUL EXCEPTIONS
        file_name = sys.argv[1]
        self.command_sequence = []
        memory_preset = []
        input_file = open(file_name,'r')
        for line in input_file:
            line = line.strip()
            if line.strip().startswith('#') or line == '':
                continue
            elif line.strip().startswith('['):
                memory_preset = line[1:-1].split(',')
            else:
                self.command_sequence.append(line.strip().upper())

        self.memory.init(memory_preset,self.command_sequence)
        self.wheel.init(self.command_sequence)

        input_file.close()

        self.run_app()
        master.destroy()

    def run_app(self):
        first = True
        for command in self.command_sequence:
            if not first:
                self.wheel.next_command()
            else:
                first = False
            if re.match('A AND B',command):
                self.logical_command(1, 1, 0)
            elif re.match('~A AND B',command):
                self.logical_command(0, 1, 0)
            elif re.match('A AND ~B',command):
                self.logical_command(1, 0, 0)
            elif re.match('~A AND ~B',command):
                self.logical_command(0, 0, 0)
            elif re.match('A OR B',command):
                self.logical_command(1, 1, 1)
            elif re.match('~A OR B',command):
                self.logical_command(0, 1, 1)
            elif re.match('A OR ~B',command):
                self.logical_command(1, 0, 1)
            elif re.match('~A OR ~B',command):
                self.logical_command(0, 0, 1)
            elif re.match('STORE [0-9]+$',command):
                self.memory_command(1,int(command[6:]))
            elif re.match('LOAD [0-9]+$',command):
                self.memory_command(0,int(command[5:]))
            else:
                print 'Invalid Command : ' + command

    def logical_command(self, A, B, opr):
        proc_switches = [self.register.A_state,self.register.B_state,1,opr,A,B,opr]
        self.processor.set_switch(proc_switches)
        self.cable.set_switch(0)
        if self.cable.switch_done.get() == 0:
            self.master.wait_variable(self.cable.switch_done)
        if self.processor.switch_done.get() == 0:
            self.master.wait_variable(self.processor.switch_done)
        self.wheel.set_flow('red')
        self.cable.set_flow('red')
        self.processor.set_flow('red')
        if opr == 0 :
            if (self.register.A_state == A) and (self.register.B_state == B):
                self.register.set_flow('red')
                self.register.set_register('A',1)
            else:
                self.register.set_register('A',0)
        else :
            if (self.register.A_state == A) or (self.register.B_state == B):
                self.register.set_flow('red')
                self.register.set_register('A',1)
            else:
                self.register.set_register('A',0)
        self.wheel.set_flow('black')
        self.cable.set_flow('black')
        self.processor.set_flow('black')
        self.register.set_flow('black')

    def memory_command(self,opr,index):
        self.cable.set_switch(1)
        self.memory_op.set_switch(opr)
        if self.cable.switch_done.get() == 0:
            self.master.wait_variable(self.cable.switch_done)
        if self.memory_op.switch_done.get() == 0:
            self.master.wait_variable(self.memory_op.switch_done)
        self.wheel.set_flow('red')
        self.cable.set_flow('red')
        self.memory_op.set_flow('red')
        self.memory_op.toggle_blink()
        self.memory.set_target(index)
        print 'mrp ' + str(opr)
        if opr == 0:
            #load sets pr = 1 and mem -> reg
            if self.register.pr_flag_state == 0:
                print 'set a'
                self.register.set_register('A',self.memory.memory[self.memory.memory_ptr])
                print 'set flag'
                self.register.set_flag(1)
                print 'flag set'
            else:
                self.register.set_register('B',self.memory.memory[self.memory.memory_ptr])
        else:
            #store value in a to memory, clear flag and register
            self.memory.set_current_cell(self.register.A_state)
            self.register.set_flag(0)
            self.register.set_register('A',0)
            self.register.set_register('B',0)
        self.wheel.set_flow('black')
        self.cable.set_flow('black')
        self.memory_op.set_flow('black')

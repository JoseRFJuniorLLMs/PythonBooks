import sys, string, os
from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename

class DBG:
    def __init__(self, master=None, popup=0):
        self.master = master
        self.filename = 'dbg.py'
        self.top   = Toplevel(master, width=600, height=400)
        self.top.title('Tkinter Explorer')
        self.top.withdraw()
        self.popup = popup
        
        self.outer = Frame(self.top, bg='gray50')

        self.upper = Frame(self.outer, bg='gray60', bd=1)

        self.tframe = Frame(self.upper, bg='gray60')
        self.input = Text(self.tframe, width=60, height=10,
                          bg='gray85', padx=15, pady=5)
        self.input.pack(side=LEFT, expand=1, fill=BOTH)
        self.scroll = Scrollbar(self.tframe, command=self.input.yview)
        self.input.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.tframe.pack(side=TOP, expand=1, fill=BOTH)
        
        self.cmdbar = Frame(self.upper, bg='gray40', bd=2, relief=SUNKEN)
        self.open = Button(self.cmdbar, text='Open...', command=self.open,
                           bg='gray20', fg='blanchedalmond')
        self.open.pack(side=LEFT, expand=0, padx=3, pady=3)
        self.save = Button(self.cmdbar, text='Save...', command=self.save,
                           bg='gray20', fg='blanchedalmond')
        self.save.pack(side=LEFT, expand=0, padx=3, pady=3)
        self.clr  = Button(self.cmdbar, text='Clear', command=self.clr,
                           bg='gray20', fg='blanchedalmond')
        self.clr.pack(side=LEFT, expand=0, padx=3, pady=3)
        self.run  = Button(self.cmdbar, text='Run', command=self.run,
                           bg='gray20', fg='green')
        self.run.pack(side=RIGHT, expand=0, padx=3, pady=3)
        Label(self.cmdbar, text='Interpreter input', bg='gray40',
              fg='blanchedalmond').pack(side=RIGHT, padx=15)

        self.cmdbar.pack(side=BOTTOM, expand=1, fill=X, padx=5, pady=5)
        self.upper.pack(expand=1, fill=BOTH, padx=5, pady=5)

        self.lower = Frame(self.outer, bg='gray60', bd=1)
        self.tframe2 = Frame(self.lower, bg='gray60')
        self.output = Text(self.tframe2, width=60, height=10,
                          bg='gray85', padx=15, pady=5,
                           state=DISABLED)
        self.output.tag_configure('out', foreground='blue')
        self.output.tag_configure('err', foreground='red')
        self.output.pack(side=LEFT, expand=1, fill=BOTH)
        self.scroll2 = Scrollbar(self.tframe2, command=self.output.yview)
        self.output.configure(yscrollcommand=self.scroll2.set)
        self.scroll2.pack(side=RIGHT, fill=Y)
        self.tframe2.pack(side=TOP, expand=1, fill=BOTH)
        
        self.cmdbar2 = Frame(self.lower, bg='gray40', bd=2, relief=SUNKEN)
        self.prt = Button(self.cmdbar2, text='Print', command=self.prt,
                           bg='gray20', fg='blanchedalmond')
        self.prt.pack(side=LEFT, expand=0, padx=3, pady=3)
        self.exit = Button(self.cmdbar2, text='Exit', command=self.master.quit,
                           bg='gray20', fg='red')
        self.exit.pack(side=RIGHT, expand=0, padx=3, pady=3)
        Label(self.cmdbar2, text='stdout/stderr output', bg='gray40',
              fg='blanchedalmond').pack(side=RIGHT, padx=15)
        self.cmdbar2.pack(side=BOTTOM, expand=1, fill=X, padx=5, pady=5)
        self.lower.pack(expand=1, fill=BOTH, padx=5, pady=5)
        self.outer.pack(expand=1, fill=BOTH)

        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = OutputWrapper(self.top, self.update, 'out',
                                   self.popup)
        sys.stderr = OutputWrapper(self.top, self.update, 'err',
                                   self.popup)

    def update(self, outstr, tag):
        self.output.configure(state=NORMAL)
        self.output.insert(END, outstr, tag)
        self.output.see(END)
        self.output.configure(state=DISABLED)

    def open(self):
        self.filename = askopenfilename()
        if self.filename:
            self.input.delete(1.0, END)
            fd = open(self.filename)
            for line in fd.readlines():
                self.input.insert(END, line)
            fd.close()

    def save(self, forPrt=None):
        script = self.input.get(1.0, END)
        if script:
            if forPrt:
                file = 'prt.tmp'
            else: 
                self.filename = file = asksaveasfilename(initialfile= \
                                                         self.filename)
            fd = open(self.file, 'w')
            for line in string.split(script, '\n'):
                fd.write(line)
                fd.write('\n')
            fd.close

    def clr(self):
        self.input.delete(1.0, END)

    def run(self, globals=None, locals=None):
        script = self.input.get(1.0, END)
        try:
            if globals is None:
                import __main__
                globals = __main__.__dict__
            if locals is None:
                locals = globals
            try:
                exec script in globals, locals
            except:
                self.update('exec failed\n\n', 'err')
        except:
            self.update('Bad exec\n\n', 'err')
    
    def prt(self):
        self.save(forPrt=1)
        os.system('copy prt.tmp PRN:')
        os.system('del prt.tmp')

class OutputWrapper:
    def __init__(self, top, callback, tag, popup):
        self.toplevel = top
        self.callback = callback
        self.tag      = tag
        self.popup    = popup
        
    def write(self, out):
        if self.tag == 'err' and self.popup:
            self.toplevel.deiconify()
        self.callback(out, self.tag)

if __name__ == '__main__':
    root = Tk()
    root.option_add('*font', ('verdana', 10, 'bold'))
    dbg = DBG(root, popup=1)
    dbg.top.deiconify()
    root.mainloop()


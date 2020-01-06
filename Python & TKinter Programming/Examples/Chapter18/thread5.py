# Display digits of pi in a window, calculating in a separate thread.
# Compare with wpi.py in the Demo/threads/wpi.py

import time, thread, random
from Tkinter import *

class ThreadExample:
    def __init__(self, master=None):
        self.ok                = 1
        self.digits            = []
        self.digits_calculated = 0
	self.digits_displayed  = 0
	self.master            = master
        
	thread.start_new_thread(self.worker_thread1, ())

        self.frame = Frame(master, relief=RAISED, borderwidth=2)
        self.text = Text(self.frame, height=26, width=50)
        self.scroll = Scrollbar(self.frame, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroll.set)
        self.text.pack(side=LEFT)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.frame.pack(padx=4, pady=4)
        self.btn = Button(master, text='Close', command=self.shutdown)
        self.btn.pack(side=TOP, pady=5)

	thread.start_new_thread(self.worker_thread2, ())
        
        self.master.after(100, self.check_digits)

    def worker_thread1(self):
	k, a, b, a1, b1 = 2l, 4l, 1l, 12l, 4l
	while self.ok:
            # Next approximation
            p, q, k = k*k, 2l*k+1l, k+1l
            a, b, a1, b1 = a1, b1, p*a+q*a1, p*b+q*b1
            # Print common digits
            d, d1 = a/b, a1/b1
            #print a, b, a1, b1
            while d == d1:
                self.digits.append(`int(d)`)
                a, a1 = 10l*(a%b), 10l*(a1%b1)
                d, d1 = a/b, a1/b1
            time.sleep(0.001)

    def worker_thread2(self):
        while self.ok:
            self.btn.configure(background=self.color())
            time.sleep(0.1)
        
    def shutdown(self):
        self.ok =0
        self.master.after(100, self.master.quit)

    def check_digits(self):
        self.digits_calculated = len(self.digits)
        diff = self.digits_calculated - self.digits_displayed
        ix = self.digits_displayed
        for i in range(diff):
            self.text.insert(END, self.digits[ix+i])
        self.digits_displayed =  self.digits_calculated   
        self.master.title('%d digits of pi' % self.digits_displayed)
        self.master.after(100, self.check_digits)

    def color(self):
        rc = random.choice
        return '#%02x%02x%02x' % (rc(range(0,255)), rc(range(0,255)),
                                  rc(range(0,255)))

root = Tk()
root.option_readfile('optionDB')
example = ThreadExample(root)
root.mainloop()

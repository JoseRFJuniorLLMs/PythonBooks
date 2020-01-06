from Tkinter import *
import sys, socket, time

class Server:
    def __init__(self):
        host = socket.gethostbyname(socket.gethostname())
	addr = host, 5000
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind('', 0)
	while 1:
            time.sleep(60.0)
            s.sendto(time.asctime(time.localtime(time.time())), addr)

class GUIClient:
    def __init__(self, master=None):
        self.master            = master
        self.master.title('Time Service Client')
        self.frame = Frame(master, relief=RAISED, borderwidth=2)
        self.text = Text(self.frame, height=26, width=50)
        self.scroll = Scrollbar(self.frame, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroll.set)
        self.text.pack(side=LEFT)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.frame.pack(padx=4, pady=4)
        Button(master, text='Close', command=self.master.quit).pack(side=TOP)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	self.socket.bind('', 5000)

	tkinter.createfilehandler(self.socket, READABLE, self.ihandler)

        self.master.after(5000, self.doMark)
        
    def ihandler(self, sock, mask):
        data, addr = sock.recvfrom(256)
        self.text.insert(END, '%s\n' % data)

    def doMark(self):
        self.text.insert(END, 'waiting...\n')
        self.master.after(5000, self.doMark)

if len(sys.argv) < 2:
    print 'select -s (server) or -c (client)'
    sys.exit(2)
if sys.argv[1] == '-s':
    server=Server()
elif sys.argv[1] == '-c':
    root = Tk()
    root.option_readfile('optionDB')
    example = GUIClient(root)
    root.mainloop()

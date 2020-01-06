from Tkinter import *
import Image, ImageTk, os, string

class Scrapbook:
    def __init__(self, master=None):
        self.master = master
        self.frame = Frame(master, width=400, height=420, bg='gray50',
                           relief=RAISED, bd=4)
              
        self.lbl = Label(self.frame)
        self.lbl.place(relx=0.5, rely=0.48, anchor=CENTER)

        self.images = []
        images = os.listdir("images")

        xpos = 0.05
        for i in range(10):
            Button(self.frame, text='%d'%(i+1), bg='gray10',
                   fg='white', command=lambda s=self, img=i: \
                       s.getImg(img)).place(relx=xpos, rely=0.99, anchor=S)
            xpos = xpos + 0.08
            self.images.append(images[i])
            
        Button(self.frame, text='Done',  command=self.exit,
               bg='red', fg='yellow').place(relx=0.99, rely=0.99, anchor=SE)
        Button(self.frame, text='Info',	 command=self.info,
	       bg='blue', fg='yellow').place(relx=0.99, rely=0.90, anchor=SE)
	self.infoDisplayed = FALSE
        self.frame.pack()
        self.getImg(0)
        
    def getImg(self, img):
        self.masterImg = Image.open(os.path.join("images",
                                                 self.images[img]))
        self.masterImg.thumbnail((350, 280))
        self.img = ImageTk.PhotoImage(self.masterImg)
        self.lbl['image'] = self.img
        
    def exit(self):
        self.master.destroy()

    def info(self):
        if self.infoDisplayed:
	    self.fm.destroy()
	    self.infoDisplayed = FALSE
        else:
	    self.fm = Frame(self.master, bg='gray10')
	    self.fm.place(in_=self.lbl, relx=0.5, relwidth=1.0, height=50,
			  anchor=S, rely=0.0, y=-4, bordermode='outside')

	    ypos = 0.15
	    for lattr in ['Format', 'Size', 'Mode']:
	        Label(self.fm, text='%s:\t%s' % (lattr,
		      getattr(self.masterImg, '%s' % string.lower(lattr))),
		      bg='gray10', fg='white',font=('verdana', 8)).place(\
		      relx=0.3, rely= ypos, anchor=W)
	        ypos = ypos + 0.35
            self.infoDisplayed = TRUE

root = Tk()
root.option_add('*font', ('verdana', 10, 'bold'))
root.title('Scrapbook')
scrapbook = Scrapbook(root)
root.mainloop()





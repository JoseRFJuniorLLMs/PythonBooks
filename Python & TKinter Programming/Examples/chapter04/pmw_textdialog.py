from Tkinter import *
import Pmw
root = Tk()
root.option_readfile('optionDB')
root.title('TextDialog')
Pmw.initialise()

sketch = """Doctor: Mr. Bertenshaw? 
Mr. B:  Me, Doctor. 
Doctor: No, me doctor, you Mr. Bertenshaw. 
Mr. B:  My wife, doctor... 
Doctor: No, your wife patient. 
Sister: Come with me, please. 
Mr. B:  Me, Sister? 
Doctor: No, she Sister, me doctor, you Mr. Bertenshaw. 
Nurse:  Dr. Walters? 
Doctor: Me, nurse...You Mr. Bertenshaw, she Sister, you doctor. 
Sister: No, doctor. 
Doctor: No doctor: call ambulance, keep warm. 
Nurse:  Drink, doctor? 
Doctor: Drink doctor, eat Sister, cook Mr. Bertenshaw, nurse me! 
Nurse:  You, doctor? 
Doctor: ME doctor!! You Mr. Bertenshaw. She Sister! 
Mr. B:  But my wife, nurse... 
Doctor: Your wife not nurse. She nurse, your wife patient. Be patient, 
        she nurse your wife. Me doctor, you tent, you tree, you Tarzan, me 
        Jane, you Trent, you Trillo...me doctor!"""

dialog = Pmw.TextDialog(root, scrolledtext_labelpos='n',
		title='Sketch',
		defaultbutton=0,
		label_text='The Hospital')
dialog.insert(END, sketch)
dialog.configure(text_state='disabled')

dialog.activate()
dialog.tkraise()

root.mainloop()


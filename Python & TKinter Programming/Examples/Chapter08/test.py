import winsound
import time

   # Play wav file 
winsound.PlaySound('c:/winnt/media/Chord.wav', winsound.SND_FILENAME)

   # Play sound from control panel settings
winsound.PlaySound('SystemQuestion', winsound.SND_ALIAS)

   # Play wav file from memory
data=open('c:/winnt/media/Chimes.wav',"rb").read()
winsound.PlaySound(data, winsound.SND_MEMORY)

   # Start playing the first bit of wav file asynchronously
winsound.PlaySound('c:/winnt/media/Chord.wav',
                   winsound.SND_FILENAME|winsound.SND_ASYNC)
   # But dont let it go for too long...
time.sleep(0.1)
   # ...Before stopping it
winsound.PlaySound(None, 0)

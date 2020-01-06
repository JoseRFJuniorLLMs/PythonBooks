# SimpleThreads.py
#
# Trivial example of using the Python threading module.

import Threading
import time
import random

class SimpleThread(Threading.Thread):
    def run(self):
        for i in range(5):
            print self, i
            time.sleep(random.random())

if __name__=='__main__':
    threads = []
    for i in range(3):
        thread = SimpleThread()
        thread.start()
        threads.append(thread)
    # Now we wait for them to finish.
    for thread in threads:
        thread.join()
    print "All threads finished"

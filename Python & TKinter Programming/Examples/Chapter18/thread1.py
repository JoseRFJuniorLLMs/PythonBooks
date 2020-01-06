import thread, time

class Server:
    def __init__(self):
        self._dispatch = {}
        self._dispatch['a'] = self.serviceA
        self._dispatch['b'] = self.serviceB
        self._dispatch['c'] = self.serviceC
        self._dispatch['d'] = self.serviceD

    def service(self, which, qual):
        self._dispatch[which](qual)

    def serviceA(self, argin):
        thread.start_new_thread(self.engine, (argin,'A'))

    def serviceB(self, argin):
        thread.start_new_thread(self.engine, (argin,'B'))

    def serviceC(self, argin):
        thread.start_new_thread(self.engine, (argin,'C'))

    def serviceD(self, argin):
        thread.start_new_thread(self.engine, (argin,'D'))

    def engine(self, arg1, arg2):
        for i in range(500):
            print '%s%s%03d' % (arg1, arg2, i),
            time.sleep(0.0001)
        print

server = Server()

server.service('a', '88')
server.service('b', '12')
server.service('c', '44')
server.service('d', '37')

time.sleep(30.0)

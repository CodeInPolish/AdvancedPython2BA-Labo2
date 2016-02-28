import socket
import sys
import threading
import pickle
import os

class Chat():
    def __init__(self, host=socket.gethostbyname("DESKTOP-UPJ8DL0"), port=5001):
        self.__s = socket.socket()
        self.__running = True
        self.__server = (host, port)
        self.__pseudo = ""
        self.serverdata = ""
        self.inputdata = []
        self.__s.connect(self.__server)
        self.cmd = { "/exit" : self._exit, "/join" : self._askServer, "NC": self._Notify, "/accept": self._Accept,
            "OC" : self._OpenConv}
        self.__s.sendall(self.GetPseudo())
    
    def run(self):
        threading.Thread(target=self._receive).start()
        threading.Thread(target=self._readinput).start()

        while(self.__running):
            if len(self.serverdata) != 0:
                self._handler(self.serverdata)
                self.serverdata = ""

            if len(self.inputdata) > 0:
                for line in self.inputdata:
                    self._handler(line)
                self.inputdata = []
            
            
    def GetPseudo(self):
        sys.stdout.write("Entrez votre pseudo: ")
        sys.stdout.flush()
        data = sys.stdin.readline().rstrip()
        self.__pseudo = data
        return data.encode()

    def _handler(self, data):

        cmd = data.split(";")[0]
        param = data.split(";")[1:]

        if cmd in self.cmd:
                self.cmd[cmd]() if len(param) == 0 else self.cmd[cmd](param)

    def _askServer(self, pseudo):
        cmd = ["NC", pseudo[0], self.__pseudo]
        self.__s.sendall( (";".join(cmd)).encode() )

    def _Notify(self, param):
        print("{} veut te parler".format(param[0]))

    def _Accept(self, param):
        print("Ouverture de la conversation avec {}".format(param[0]))
        data = "C2C;" + param[0] + ";" + self.__pseudo
        self.__s.sendall(data.encode())

    def _OpenConv(self, param):
        os.system("start python chat.py " + "{} {} {}".format(param[1], param[2], param[3]))
    
    def _exit(self):
        self.__s.sendall( ("DfS;"+self.__pseudo).encode() )
        self.__s.shutdown(socket.SHUT_WR)
        self.__s.recv(1024).decode()
        self.__s.close()
        self.__running = False
        pass
    
    def _receive(self):
        while self.__running:
            try:
                data = self.__s.recv(1024)
                self.serverdata = data.decode()
            except socket.timeout:
                pass
            except OSError:
                pass

    def _readinput(self):
        while(True):
            self.inputdata.append(sys.stdin.readline().rstrip())

if __name__ == '__main__':
    if len(sys.argv) == 3:
        Chat(sys.argv[1], int(sys.argv[2])).run()
    else:
        Chat().run()

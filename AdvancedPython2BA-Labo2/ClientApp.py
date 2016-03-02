import socket
import sys
import threading
import pickle
import os

class Chat():
    def __init__(self, host=socket.gethostbyname("DESKTOP-UPJ8DL0"), port=5001, pseudo=""):
        self.s = socket.socket()
        self.running = True
        self.server = (host, port)
        self.pseudo = pseudo
        self.serverdata = []
        self.inputdata = []
        self.s.connect(self.server)
        self.cmd = { "/exit" : self._exit, "/join" : self._askServer, "/accept": self._Accept, 
                    "/users" : self._CheckUsers}
        self.servercmd = { "NC" : self._Notify, "OC" : self._OpenConv, "LU" : self._listusers }
        self.s.sendall(self.GetPseudo())
    
    def run(self):
        threading.Thread(target=self._receive).start()
        threading.Thread(target=self._readinput).start()

        while(self.running):
            self._execmd(self.serverdata, self.servercmd)
            self._execmd(self.inputdata, self.cmd)
            
            
    def GetPseudo(self):
        if(self.pseudo == ""):
            sys.stdout.write("Entrez votre pseudo: ")
            sys.stdout.flush()
            data = sys.stdin.readline().rstrip()
            self.pseudo = data
            return data.encode()
        return self.pseudo.encode()

    def _execmd(self, source, cmd_list):
        if len(source) != 0:
            source.reverse()
            for cmd in source:
                self._handler(source.pop(), cmd_list)

    def _handler(self, data, cmds):

        cmd = data.split(" ")[0]
        param = data.split(" ")[1:]

        if cmd in cmds:
                cmds[cmd]() if len(param) == 0 else cmds[cmd](param)

    def _askServer(self, pseudo):
        cmd = ["NC", pseudo[0], self.pseudo]
        self.s.sendall( (" ".join(cmd)).encode() )

    def _CheckUsers(self):
        cmd = ["CU", self.pseudo]
        self.s.sendall( (" ".join(cmd)).encode() )

    def _listusers(self, param):
        print("Connected clients: ")
        for client in param:
            if client != self.pseudo:
                print("   ->{}".format(client))

    def _Notify(self, param):
        print("{} veut te parler".format(param[0]))

    def _Accept(self, param):
        data = "C2C " + param[0] + " " + self.pseudo
        self.s.sendall(data.encode())

    def _OpenConv(self, param):
        print("Ouverture de la conversation avec {}".format(param[0]))
        os.system("start python chat.py " + "{} {} {} {} {}".format(param[1], param[0], self.pseudo, param[2], param[3]))
    
    def _exit(self):
        self.s.sendall( ("DfS "+self.pseudo).encode() )
        self.s.shutdown(socket.SHUT_WR)
        self.s.recv(1024).decode()
        self.s.close()
        self.running = False
        print("Vous pouvez fermer l'appli")
        pass
    
    def _receive(self):
        while self.running:
            try:
                data = self.s.recv(1024)
                self.serverdata.append(data.decode())
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
    elif len(sys.argv) == 4:
        Chat(sys.argv[1], int(sys.argv[2]), sys.argv[3]).run()
    else:
        Chat().run()

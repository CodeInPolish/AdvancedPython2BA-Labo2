import socket
import select
import time 
import pickle
import os

SERVERADDRESS = (socket.gethostname(), 5001)

class EchoServer():
    def __init__(self):
        self.s = socket.socket()
        self.once = True
        self.timeout = 0.05
        self.ServerRunning = False
        self.cmds = {"DfS" : self._DisconnectFromServer, "NC" : self._NotifyClient, "C2C" : self._Connect2Client}
        self.AllocatedPorts = []
        self.WaitingClients = []
        self.ConnectedClients = {}
        self.NotifiedClients = []
        self.s.bind(SERVERADDRESS)
        self.s.listen(5)

    def listening(self):
        self.WaitingClients = select.select([self.s], (), (), self.timeout)[0]

        if len(self.WaitingClients) != 0:
            self.once = True
            self._Connect2Server()

        if len(self.ConnectedClients) != 0:
            Clients_to_read = select.select( list(self.ConnectedClients.values()), (), (), self.timeout)[0]
            for client in Clients_to_read:
                cmd, param = self._receivecmd(client)
                print(cmd)
                print(param)
                if cmd in self.cmds:
                    self.cmds[cmd]() if len(param) == 0 else self.cmds[cmd](param)
                else:
                    print(cmd+" ".join(param))       

    def _Connect2Server(self):
        for client in self.WaitingClients:
            sock, ip = client.accept()
            self.ConnectedClients[self._receive(sock)]= sock

    def _DisconnectFromServer(self, param):
        pseudo = param[0]
        self.ConnectedClients[pseudo].shutdown(socket.SHUT_WR)
        del self.ConnectedClients[pseudo]
        print(self.ConnectedClients.keys())

    def _NotifyClient(self, param):
        data = "NC;" + param[1]
        self.ConnectedClients[param[0]].send(data.encode())

    def _Connect2Client(self, param):
        #data = "start python chat.py " + ip + " 6500"
        ip = "192.168.0.135"
        port0 = "5002"
        port1 = "5003"

        data = "OC;{};{};{};{}".format(param[1], ip, port0, port1)
        self.ConnectedClients[param[0]].sendall(data.encode())
        data = "OC;{};{};{};{}".format(param[0], ip, port1, port0)
        self.ConnectedClients[param[1]].sendall(data.encode())


    def run(self):
        while True:
            self.listening()
            if len(self.ConnectedClients) != 0 and self.once == True:
                print(self.ConnectedClients.keys())
                #os.system("start python chat.py " + "172.17.33.243 6500")
                self.once=False
    
    def _receive(self, client):
        data = client.recv(1024)
        return data.decode()

    def _receivecmd(self, client):
        data = self._receive(client)
        data = data.split(";")
        return ( data[0], data[1:])

Server = EchoServer()
Server.run()

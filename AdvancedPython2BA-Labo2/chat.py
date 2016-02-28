#!/usr/bin/env python3
# chat.py
# author: Hadrien Hachez
# version: February 16, 2016
import socket
import sys
import threading
import time

class Chat():
    
    def __init__(self, client, port=6001, port_c=6002):
        s = socket.socket(type=socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.bind((socket.gethostname(), port))
        self.__s = s
        self.__address = (client, port_c)
        print('Écoute sur {}:{}'.format(socket.gethostname(), port))

    def run(self):
        handlers = {
            '/exit': self._exit,
            '/quit': self._quit
        }

        self.__running = True
        threading.Thread(target=self._receive).start()
        while self.__running:
            line = sys.stdin.readline().rstrip() + ' '
            # Extract the command and the param
            command = line[:line.index(' ')]
            param = line[line.index(' ')+1:].rstrip()
            # Call the command handler
            if command in handlers:
                try:
                    handlers[command]() if param == '' else handlers[command](param)
                except:
                    print("Erreur lors de l'exécution de la commande.")
            else:
                self._send(command+' '+param)

    def _exit(self):
        self.__running = False
        self.__address = None
        self.__s.close()

    def _quit(self):
        self.__address = None

    def _send(self, param):
        if self.__address is not None:
            try:
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__address)
                    totalsent += sent
            except OSError:
                print('Erreur lors de la réception du message.')

    def _receive(self):
        while self.__running:
            try:
                data, address = self.__s.recvfrom(1024)
                print(address[0]+' ({}:{:0>2}): '.format(time.localtime()[3],time.localtime()[4]) + data.decode())
            except socket.timeout:
                pass
            except OSError:
                return

if __name__ == '__main__':
    if len(sys.argv) == 4:
        Chat(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])).run()
    else:
        Chat().run()

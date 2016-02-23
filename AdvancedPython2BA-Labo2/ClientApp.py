import socket
import sys
import threading
import pickle

class Chat():
    def __init__(self, host=socket.gethostbyname("DESKTOP-UPJ8DL0"), port=5001):
        self.__s = socket.socket()
        self.__server = (host, port)
        self.__pseudo = ""
        print('Écoute sur {}:{}'.format(socket.gethostbyname(socket.gethostname), port))
    
    def run(self):
        threading.Thread(target=self._receive).start()

    def GetPseudo(self):
        sys.stdout.write("Entrez votre pseudo: ")
        sys.stdout.flush()
        data = sys.stdin.readline().rstrip()
    
    def _exit(self):
        #commande à envoyer au serveur pour quitter l'appli chat
        pass
    
    def _quit(self):
        #on verra
        pass
    
    def _send(self, param):
        #à réecrire
        pass
    
    def _receive(self):
        while self.__running:
            try:
                data = self.__s.recv(1024)
                print(data.decode())
            except socket.timeout:
                pass
            except OSError:
                return
"""
if __name__ == '__main__':
    if len(sys.argv) == 3:
        Chat(sys.argv[1], int(sys.argv[2])).run()
    else:
        Chat().run()
"""
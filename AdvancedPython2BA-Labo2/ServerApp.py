import socket

SERVERADDRESS = (socket.gethostname(), 6000)

class EchoServer():
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        
    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            try:
                print(self._receive(client).decode())
                client.close()
            except OSError:
                print('Erreur lors de la réception du message.')
    
    def _receive(self, client):
        chunks = []
        finished = False
        while not finished:
            data = client.recv(1024)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)

s = socket.socket(type=socket.SOCK_DGRAM)
s.bind(("localhost", 5000))
data=s.recvfrom(512)
print("Reçu {} octets de {}".format(len(data[0].decode()), data[1]))
print("Data:", data[0].decode())
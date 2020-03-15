import socket
import threading
from time import sleep


class DNSServer:
    LOOP_UP_SERVER = ['8.8.8.8', '8.8.4.4', '9.9.9.9', '149.112.112.112']
    SERVER_CONNECTION_POLL_INTERVAL = 0.1
    SERVER_CLIENT_POLL_INTERVAL = 0.2
    # Default receive size set to max DNS request size
    RECEIVE_SIZE = 512

    def __init__(self, socket_famlily=socket.AF_INET, socket_type=socket.SOCK_DGRAM, port=53, interfaces=''):
        # Start UDP IP socket on port 53 for DNS
        self.udps = socket.socket(socket_famlily, socket_type)
        self.udps.bind((interfaces, port))

        self.alive = True

        self.mapped_cache = []

        self.connection_poll_thread = None

        self.start_connection_polling()

    def start_connection_polling(self):
        self.connection_poll_thread = threading.Thread(target=self._connection_poll)
        self.connection_poll_thread.start()

    def _connection_poll(self):
        message = ''
        while self.alive:
            sleep(self.SERVER_CONNECTION_POLL_INTERVAL)
            data, server = self.udps.recvfrom(self.RECEIVE_SIZE)

            print(data)
            print(server)

            response = self.resolve(data)

            self.udps.sendto(response, server)

    def resolve(self, hostname):
        pass


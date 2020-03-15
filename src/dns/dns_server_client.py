import threading
from time import sleep


class DNSServerClient:
    CLIENT_POLL_INTERVAL = 0.1
    RECEIVE_SIZE = 1024
    MESSAGE_END = '<END>'

    def __init__(self, client_connection, address=None):
        print('Created user from {}'.format(address))
        self.client_connection = client_connection
        self.address = address

        self.done_handshake = False

        self.poll_thread = None
        # Variable to stop the poll threads
        self.alive = True

        self.inbox = []

        self.start_polling()

    def get_handshake_done(self):
        return self.done_handshake

    def handshake_done(self):
        self.done_handshake = True

    def is_alive(self):
        return self.alive

    def kill(self):
        self.alive = False

    def set_address(self, address):
        self.address = address

    def get_address(self):
        return self.address

    def get_next_message(self):
        if self.inbox:
            return self.inbox.pop(0)
        else:
            return None

    def start_polling(self):
        self.poll_thread = threading.Thread(target=self._client_poll)
        self.poll_thread.start()

    def _client_poll(self):
        message = ''
        while self.alive:
            sleep(self.CLIENT_POLL_INTERVAL)
            try:
                data = self.client_connection.recv(self.RECEIVE_SIZE)
                message += data.decode()

                # Detect closed socket
                if not data:
                    self.alive = False

                print(message)

                # For messages lager than the buffer, search for the message end.
                if self.MESSAGE_END not in message:
                    continue

                print('Received {} from {}'.format(message, self.address))

                self.inbox.append(message)
            except Exception as e:
                print('Failed receiving, did the connection close? {}'.format(e))
                self.alive = False

            # Reset message for next message
            message = ''

    def send(self, message):
        """
        Send a message to this client
        :param message: The message to send
        :return: None
        """
        print('Sending: {}'.format(message))
        try:
            self.client_connection.sendall(str.encode(message))
        except Exception as e:
            print('Failed sending message: {} to: {}'.format(message, self.address))

    def __str__(self):
        return '{} alive: {}'.format(self.address, self.alive)

    def __del__(self):
        self.alive = False
        self.client_connection.close()

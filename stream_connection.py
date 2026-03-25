import socket
import json

class DataStreamer:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect_to_stream(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
            return True
        except ConnectionRefusedError:
            return False

    def receive_stream(self):
        if not self.client_socket:
            return

        try:
            while True:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                
                message = data.decode('utf-8')
                for line in message.strip().split('\n'):
                    if not line.strip():
                        continue
                    
                    try:
                        json_record = json.loads(line)
                        print(json_record)
                    except json.JSONDecodeError:
                        continue
                        
        except KeyboardInterrupt:
            pass
        finally:
            self.client_socket.close()

if __name__ == "__main__":
    streamer = DataStreamer()
    if streamer.connect_to_stream():
        streamer.receive_stream()
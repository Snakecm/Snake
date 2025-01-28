# Network support for multiplayer mode
import socket
import json
import threading
from typing import Optional, Dict, Callable
from dataclasses import asdict, dataclass

@dataclass
class NetworkMessage:
    type: str
    data: dict
    player_id: str

class NetworkManager:
    def __init__(self, host: str = "localhost", port: int = 5000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients: Dict[str, socket.socket] = {}
        self.handlers: Dict[str, Callable] = {}
        self.running = False
    
    def start_server(self) -> None:
        self.socket.bind((self.host, self.port))
        self.socket.listen(4)  # Maximum 4 players
        self.running = True
        
        # Start listening thread
        thread = threading.Thread(target=self._accept_connections)
        thread.daemon = True
        thread.start()
    
    def connect_to_server(self, player_id: str) -> bool:
        try:
            self.socket.connect((self.host, self.port))
            self.clients[player_id] = self.socket
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def send_message(self, message: NetworkMessage) -> None:
        data = json.dumps(asdict(message))
        if message.player_id in self.clients:
            self.clients[message.player_id].send(data.encode())
    
    def register_handler(self, message_type: str, handler: Callable) -> None:
        self.handlers[message_type] = handler
    
    def _accept_connections(self) -> None:
        while self.running:
            client, addr = self.socket.accept()
            thread = threading.Thread(target=self._handle_client, args=(client,))
            thread.daemon = True
            thread.start()
    
    def _handle_client(self, client: socket.socket) -> None:
        while self.running:
            try:
                data = client.recv(1024).decode()
                if not data:
                    break
                    
                message = json.loads(data)
                if message["type"] in self.handlers:
                    self.handlers[message["type"]](message)
            except:
                break
        
        client.close() 
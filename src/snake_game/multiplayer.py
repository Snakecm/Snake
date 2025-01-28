# Multiplayer game mode implementation
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from .core import Position, Snake
from .events import GameEvent, EventType
from .config import GameConfig

@dataclass
class Player:
    id: str
    name: str
    snake: Snake
    score: int = 0
    is_alive: bool = True
    color: Tuple[int, int, int] = (0, 255, 0)

class MultiplayerManager:
    def __init__(self, config: GameConfig):
        self.players: Dict[str, Player] = {}
        self.config = config
        self.event_handlers = []
    
    def add_player(self, player_id: str, name: str, start_pos: Position) -> Player:
        player = Player(
            id=player_id,
            name=name,
            snake=Snake(start_pos)
        )
        self.players[player_id] = player
        return player
    
    def remove_player(self, player_id: str) -> None:
        if player_id in self.players:
            del self.players[player_id]
    
    def update(self, dt: float) -> List[GameEvent]:
        events = []
        # Check collisions between snakes
        for player_id, player in self.players.items():
            if not player.is_alive:
                continue
                
            head = player.snake.get_head()
            # Check collision with other snakes
            for other_id, other in self.players.items():
                if player_id == other_id:
                    continue
                    
                if head in other.snake.body:
                    player.is_alive = False
                    events.append(GameEvent(
                        type=EventType.COLLISION,
                        position=head
                    ))
        
        return events
    
    def get_player_positions(self) -> List[Tuple[Position, Tuple[int, int, int]]]:
        positions = []
        for player in self.players.values():
            if player.is_alive:
                for pos in player.snake.body:
                    positions.append((pos, player.color))
        return positions 
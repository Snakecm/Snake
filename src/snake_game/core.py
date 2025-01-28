# Core game logic and classes
from typing import List, Tuple, Optional
import random

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Snake:
    def __init__(self, start_position: Position, initial_length: int = 3):
        self.body: List[Position] = [start_position]
        self.direction = (1, 0)  # Default moving right
        self.initial_length = initial_length
        
    def move(self, new_head: Position) -> None:
        self.body.insert(0, new_head)
        if len(self.body) > self.initial_length:
            self.body.pop()
            
    def get_head(self) -> Position:
        return self.body[0]

class GameState:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.snake = Snake(Position(width // 2, height // 2))
        self.food = self._generate_food()
        self.score = 0
        self.is_game_over = False
    
    def _generate_food(self) -> Position:
        while True:
            food = Position(
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1)
            )
            if not any(food == pos for pos in self.snake.body):
                return food 
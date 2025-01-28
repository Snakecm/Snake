# Game engine and main loop logic
from .core import GameState, Position

class GameEngine:
    def __init__(self, width: int = 20, height: int = 20):
        self.state = GameState(width, height)
    
    def update(self) -> bool:
        """
        Update game state for one frame
        Returns: True if game continues, False if game over
        """
        if self.state.is_game_over:
            return False
            
        # Calculate new head position
        current_head = self.state.snake.get_head()
        new_head = Position(
            current_head.x + self.state.snake.direction[0],
            current_head.y + self.state.snake.direction[1]
        )
        
        # Check collision with walls
        if (new_head.x < 0 or new_head.x >= self.state.width or
            new_head.y < 0 or new_head.y >= self.state.height):
            self.state.is_game_over = True
            return False
            
        # Check collision with self
        if any(new_head == pos for pos in self.state.snake.body):
            self.state.is_game_over = True
            return False
            
        # Move snake
        self.state.snake.move(new_head)
        
        # Check food collision
        if new_head == self.state.food:
            self.state.score += 1
            self.state.snake.initial_length += 1
            self.state.food = self.state._generate_food()
            
        return True 
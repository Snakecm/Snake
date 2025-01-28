# Save system for game state persistence
import json
import os
from dataclasses import asdict
from typing import Dict, Any, Optional
from datetime import datetime
from .core import Position, GameState
from .scoring import ScoreManager

class SaveManager:
    def __init__(self, save_dir: str = "saves"):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
    
    def save_game(self, state: GameState, score_manager: ScoreManager, name: Optional[str] = None) -> str:
        # Generate save name if not provided
        if name is None:
            name = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        save_data = {
            "snake": {
                "body": [(pos.x, pos.y) for pos in state.snake.body],
                "direction": state.snake.direction,
                "length": state.snake.initial_length
            },
            "food": {
                "position": (state.food.x, state.food.y)
            },
            "score": {
                "current": score_manager.current_score,
                "high": score_manager.high_score,
                "achievements": [
                    asdict(achievement) 
                    for achievement in score_manager.achievements
                ]
            },
            "dimensions": {
                "width": state.width,
                "height": state.height
            }
        }
        
        filepath = os.path.join(self.save_dir, f"{name}.json")
        with open(filepath, "w") as f:
            json.dump(save_data, f, indent=2)
        
        return filepath
    
    def load_game(self, name: str) -> tuple[GameState, ScoreManager]:
        filepath = os.path.join(self.save_dir, f"{name}.json")
        with open(filepath, "r") as f:
            save_data = json.load(f)
        
        # Reconstruct game state
        state = GameState(
            save_data["dimensions"]["width"],
            save_data["dimensions"]["height"]
        )
        
        # Restore snake
        state.snake.body = [
            Position(x, y) for x, y in save_data["snake"]["body"]
        ]
        state.snake.direction = tuple(save_data["snake"]["direction"])
        state.snake.initial_length = save_data["snake"]["length"]
        
        # Restore food
        fx, fy = save_data["food"]["position"]
        state.food = Position(fx, fy)
        
        # Restore score manager
        score_manager = ScoreManager()
        score_manager.current_score = save_data["score"]["current"]
        score_manager.high_score = save_data["score"]["high"]
        
        return state, score_manager 
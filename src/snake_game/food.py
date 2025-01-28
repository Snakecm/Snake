# Different types of food items
from enum import Enum
from dataclasses import dataclass
from typing import Tuple
from .core import Position

class FoodType(Enum):
    NORMAL = "normal"       # Regular food
    GOLDEN = "golden"       # Worth more points
    SPEED = "speed"         # Increases snake speed
    SLOW = "slow"          # Decreases snake speed
    GHOST = "ghost"        # Allows passing through walls once
    SHRINK = "shrink"      # Reduces snake length

@dataclass
class Food:
    position: Position
    food_type: FoodType
    points: int
    color: Tuple[int, int, int]
    duration: float = 0.0  # Duration of effect in seconds
    probability: float = 1.0  # Spawn probability

class FoodFactory:
    def __init__(self):
        self.food_types = {
            FoodType.NORMAL: Food(
                position=Position(0, 0),  # Placeholder
                food_type=FoodType.NORMAL,
                points=1,
                color=(255, 0, 0),
                probability=0.7
            ),
            FoodType.GOLDEN: Food(
                position=Position(0, 0),
                food_type=FoodType.GOLDEN,
                points=5,
                color=(255, 215, 0),
                probability=0.1
            ),
            FoodType.SPEED: Food(
                position=Position(0, 0),
                food_type=FoodType.SPEED,
                points=2,
                color=(0, 255, 255),
                duration=5.0,
                probability=0.1
            ),
            FoodType.GHOST: Food(
                position=Position(0, 0),
                food_type=FoodType.GHOST,
                points=2,
                color=(200, 200, 200),
                duration=3.0,
                probability=0.05
            )
        }
    
    def create_food(self, position: Position, food_type: FoodType) -> Food:
        template = self.food_types[food_type]
        return Food(
            position=position,
            food_type=template.food_type,
            points=template.points,
            color=template.color,
            duration=template.duration,
            probability=template.probability
        ) 
# Obstacle system for additional challenge
from enum import Enum
from dataclasses import dataclass
from typing import List, Set, Tuple, Optional
from .core import Position

class ObstacleType(Enum):
    WALL = "wall"           # Solid wall
    PORTAL = "portal"       # Teleports snake
    SPIKES = "spikes"       # Deadly on touch
    TEMPORARY = "temporary" # Appears/disappears

@dataclass
class Obstacle:
    position: Position
    obstacle_type: ObstacleType
    color: Tuple[int, int, int]
    is_active: bool = True
    duration: float = 0.0   # For temporary obstacles
    portal_exit: Position = None  # For portals

class ObstacleManager:
    def __init__(self):
        self.obstacles: List[Obstacle] = []
        self.portal_pairs: List[Tuple[Position, Position]] = []
    
    def add_obstacle(self, obstacle: Obstacle) -> None:
        self.obstacles.append(obstacle)
        if obstacle.obstacle_type == ObstacleType.PORTAL and obstacle.portal_exit:
            self.portal_pairs.append((obstacle.position, obstacle.portal_exit))
    
    def check_collision(self, position: Position) -> Tuple[bool, ObstacleType]:
        for obstacle in self.obstacles:
            if obstacle.is_active and position == obstacle.position:
                return True, obstacle.obstacle_type
        return False, None
    
    def get_portal_exit(self, position: Position) -> Optional[Position]:
        for entry, exit in self.portal_pairs:
            if position == entry:
                return exit
        return None
    
    def update(self, dt: float) -> None:
        # Update temporary obstacles
        for obstacle in self.obstacles:
            if obstacle.obstacle_type == ObstacleType.TEMPORARY:
                obstacle.duration -= dt
                if obstacle.duration <= 0:
                    obstacle.is_active = not obstacle.is_active
                    obstacle.duration = 5.0  # Reset duration 
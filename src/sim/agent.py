import pygame
import numpy as np
from enum import Enum
# Initialize pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
PREDATOR_COLOR = (255, 0, 0)
PREY_COLOR = (0, 255, 0)

# Define the Predator and Prey classes


class Agent:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = np.random.rand() * 2 * np.pi

    def move(self, speed=1):
        self.x += speed * np.cos(self.direction)
        self.y += speed * np.sin(self.direction)

        # Boundaries
        self.x = np.clip(self.x, 0, WIDTH)
        self.y = np.clip(self.y, 0, HEIGHT)

    def display(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)


class Predator(Agent):
    def __init__(self, x, y):
        super().__init__(x, y, PREDATOR_COLOR)

    def move_towards(self, target, speed=1):
        angle_to_target = np.arctan2(target.y - self.y, target.x - self.x)
        self.direction = angle_to_target
        self.move(speed)


class Prey(Agent):
    def __init__(self, x, y):
        super().__init__(x, y, PREY_COLOR)

    def move_away_from(self, target, speed=1):
        angle_to_target = np.arctan2(self.y - target.y, self.x - target.x)
        self.direction = angle_to_target
        self.move(speed)


class AgentTypes(str, Enum):
    PREDATOR = "Predator"
    PREY = "Prey"


class AgentFactory:

    @staticmethod
    def create_agent(agent_type: AgentTypes, x: int, y: int):
        if agent_type == AgentTypes.PREDATOR:
            return Predator(x, y)
        elif agent_type == AgentTypes.PREY:
            return Prey(x, y)
        else:
            raise ValueError("Invalid agent type")
# Update in the Agent class



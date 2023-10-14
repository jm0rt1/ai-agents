import logging
import logging.handlers
from src.shared.settings import GlobalSettings
from src.sim.agent import Agent, AgentFactory, AgentTypes, WIDTH, HEIGHT
import numpy as np

import pygame


def initialize_logging():

    file_handler = logging.handlers.RotatingFileHandler(
        GlobalSettings.GLOBAL_LOGS_DIR/GlobalSettings.LoggingParams.GLOBAL_FILE_NAME,
        backupCount=GlobalSettings.LoggingParams.BACKUP_COUNT)

    logging.getLogger().addHandler(file_handler)
    file_handler.doRollover()
    logging.info("Global Logging Started")


def main():
    """run a console menu that has two options, runs in a while loop so multiple options can be selected"""

    initialize_logging()
    # Using the factory to create predator and prey
    predator = AgentFactory.create_agent(
        AgentTypes.PREDATOR, WIDTH / 2, HEIGHT / 2)
    prey = AgentFactory.create_agent(
        AgentTypes.PREY, np.random.randint(WIDTH), np.random.randint(HEIGHT))

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Predator and Prey Simulation")

    running = True
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move agents
        predator.move()
        prey.move()

        # Display agents
        predator.display(screen)
        prey.display(screen)

        # Update in the while loop
        predator.move_towards(prey)
        prey.move_away_from(predator)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

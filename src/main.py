import logging
import logging.handlers
from src.shared.settings import GlobalSettings
from src.sim.agent import Agent, AgentFactory, AgentTypes, WIDTH, HEIGHT
import numpy as np

import pygame

# for example, after 5 seconds if the loop runs 60 times a second
REPLICATION_THRESHOLD = 69


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
    predators = [AgentFactory.create_agent("Predator", WIDTH / 2, HEIGHT / 2)]

    preys = [AgentFactory.create_agent(
        "Prey", np.random.randint(WIDTH), np.random.randint(HEIGHT))]

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Predator and Prey Simulation")

    running = True
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for predator in predators:
            # Choose the closest prey for each predator
            closest_prey = min(preys, key=lambda prey: np.sqrt(
                (predator.x - prey.x)**2 + (predator.y - prey.y)**2))
            predator.move_towards(closest_prey)

        # Move each prey and increase their lifetime
        for prey in preys:
            prey.move_away_from(predator)
            prey.lifetime += 1

            if predator.can_eat(prey):
                preys.remove(prey)
            elif prey.lifetime > REPLICATION_THRESHOLD:
                # Replicate the prey and reset its lifetime
                new_prey = AgentFactory.create_agent(
                    "Prey", np.random.randint(WIDTH), np.random.randint(HEIGHT))
                preys.append(new_prey)
                prey.lifetime = 0
            prey.display(screen)
        if predator.can_eat(prey):
            # Respawn prey to a random location
            prey.x = np.random.randint(WIDTH)
            prey.y = np.random.randint(HEIGHT)

        # Display agents
        predator.display(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

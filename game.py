import pygame

from pygame import display, Surface
from config import KeyBinds, Config

pygame.init()
game_display = display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.RESIZABLE)
vec = pygame.math.Vector2
frames_per_second = pygame.time.Clock()


class GameObject:
    def __init__(self, positions, size, colour):
        self.surface = Surface(vec(size))
        self.surface.fill(colour)
        self.rectangle = self.surface.get_rect()
        self.rectangle.center = vec(positions)

        self.velocity = vec(5, 0)
        self.acceleration = vec(0, 0)

    def draw(self):
        return self.surface, self.rectangle


class Ball(GameObject):
    def __init__(self, positions, size=Config.BALL_SIZE, colour=Config.BALL_COLOUR):
        super().__init__(positions, size, colour)


class Player(GameObject):
    def __init__(self, positions, size=Config.PLAYER_SIZE, colour=Config.PLAYER_COLOUR):
        super().__init__(positions, size, colour)
        self.dead = False
        self.score = 0


class Environment:
    def __init__(self):
        self.players = [Player((0, Config.SCREEN_HEIGHT // 2 - 10)),
                        Player((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT // 2))]
        self.ball = Ball((Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2))

    def account_for_collision(self):
        for player in self.players:
            if player.rectangle.colliderect(self.ball.rectangle):
                player.score += 1
                return (self.ball.rectangle.centery - player.rectangle.centery) / (Config.PLAYER_SIZE[1] // 2)

    @staticmethod
    def account_for_y_collision(game_object):
        """
        Prevents game_object from going out-of-bounds in Y-axis by correcting its position.
        :param game_object: Object of type GameObject.
        """
        min_y = 0
        max_y = game_display.get_height()
        if game_object.rectangle.bottom >= max_y:
            game_object.rectangle.bottom = max_y - 1
        if game_object.rectangle.top <= min_y:
            game_object.rectangle.top = min_y + 1

    def get_keys(self):
        keys = pygame.key.get_pressed()
        if keys[KeyBinds.UP_PLAYER_1] or keys[KeyBinds.DOWN_PLAYER_1]:
            self.update_player(self.players[0], [keys[KeyBinds.UP_PLAYER_1], keys[KeyBinds.DOWN_PLAYER_1]])
        if keys[KeyBinds.UP_PLAYER_2] or keys[KeyBinds.DOWN_PLAYER_2]:
            self.update_player(self.players[1], [keys[KeyBinds.UP_PLAYER_2], keys[KeyBinds.DOWN_PLAYER_2]])

    @staticmethod
    def update_player(player, keys):
        if keys[0] >= 0.5:
            player.rectangle.centery -= Config.PLAYER_SPEED
        elif keys[1] >= 0.5:
            player.rectangle.centery += Config.PLAYER_SPEED

    def update_ball(self):
        collision = self.account_for_collision()
        if collision is not None:
            self.ball.velocity.x = -self.ball.velocity.x
            self.ball.velocity.y = collision * 10 + self.ball.velocity.y
        self.ball.rectangle.center += self.ball.velocity
        if self.ball.rectangle.bottom >= Config.SCREEN_HEIGHT or self.ball.rectangle.top <= 0:
            self.ball.velocity.y = -self.ball.velocity.y

    def render_environment(self):
        game_display.fill((0, 0, 0))
        for player in self.players:
            game_display.blit(*player.draw())
        game_display.blit(*self.ball.draw())
        display.update()


if __name__ == "__main__":
    environment = Environment()
    while True:
        environment.update_ball()
        environment.get_keys()
        environment.render_environment()
        pygame.event.pump()
        frames_per_second.tick(60)

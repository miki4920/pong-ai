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

        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

    def draw(self):
        return self.surface, self.rectangle


class Ball(GameObject):
    def __init__(self, positions, size=Config.BALL_SIZE, colour=Config.BALL_COLOUR, speed=Config.BALL_SPEED):
        super().__init__(positions, size, colour)
        self.velocity.x = speed


class Player(GameObject):
    def __init__(self, positions, size=Config.PLAYER_SIZE, colour=Config.PLAYER_COLOUR):
        super().__init__(positions, size, colour)
        self.dead = False
        self.score = 0


class Environment:
    def __init__(self):
        self.players = [Player((0, Config.SCREEN_HEIGHT // 2)),
                        Player((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT // 2))]
        self.ball = Ball((Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2))

    def account_for_collision(self):
        for player in self.players:
            if player.rectangle.colliderect(self.ball.rectangle):
                # Rewards AI algorithm for successfully bouncing the ball
                player.score += Config.PLAYER_SCORE_FOR_BOUNCE
                # TODO: Better system for determining angle of bounce
                return (self.ball.rectangle.centery - player.rectangle.centery) / (Config.PLAYER_SIZE[1])

    @staticmethod
    def collision_with_lower_bound(game_object, change):
        min_y = 0
        return game_object.rectangle.top + change <= min_y

    @staticmethod
    def collision_with_upper_bound(game_object, change):
        max_y = game_display.get_height()
        return game_object.rectangle.bottom + change >= max_y

    def get_keys(self):
        keys = pygame.key.get_pressed()
        if keys[KeyBinds.UP_PLAYER_1] or keys[KeyBinds.DOWN_PLAYER_1]:
            self.update_player(self.players[0], [keys[KeyBinds.UP_PLAYER_1], keys[KeyBinds.DOWN_PLAYER_1]])
        if keys[KeyBinds.UP_PLAYER_2] or keys[KeyBinds.DOWN_PLAYER_2]:
            self.update_player(self.players[1], [keys[KeyBinds.UP_PLAYER_2], keys[KeyBinds.DOWN_PLAYER_2]])

    def update_player(self, player, keys):
        change = 0
        if keys[0] >= 0.5 and not self.collision_with_lower_bound(player, -Config.PLAYER_SPEED):
            change = -Config.PLAYER_SPEED
        elif keys[1] >= 0.5 and not self.collision_with_upper_bound(player, Config.PLAYER_SPEED):
            change = Config.PLAYER_SPEED
        player.rectangle.centery += change

    def update_ball(self):
        if self.collision_with_upper_bound(self.ball, self.ball.velocity.y) or self.collision_with_lower_bound(self.ball, self.ball.velocity.y):
            self.ball.velocity.y = -self.ball.velocity.y
        self.ball.rectangle.center += self.ball.velocity
        collision = self.account_for_collision()
        if collision is not None:
            self.ball.velocity.x = -self.ball.velocity.x
            self.ball.velocity.y = collision * 10 + self.ball.velocity.y

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

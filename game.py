import pygame

from pygame import display, Surface

from config import Config

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
        self.velocity.y = 5
        self.previous_collision = None


class Player(GameObject):
    def __init__(self, positions, size=Config.PLAYER_SIZE, colour=Config.PLAYER_COLOUR):
        super().__init__(positions, size, colour)
        self.score = 0


class Environment:
    def __init__(self):
        self.player_groups = []

    def create_player_group(self):
        self.player_groups.append({"players": [Player((0, Config.SCREEN_HEIGHT // 2)),
                                               Player((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT // 2))],
                                   "ball": Ball((Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2)), "dead": False})

    @staticmethod
    def collision_between_players_and_ball(player_group):
        ball = player_group["ball"]
        for player in player_group["players"]:
            if ball.rectangle.colliderect(player.rectangle):
                if ball.previous_collision is player:
                    player_group["dead"] = True
                else:
                    player.score += 1
                    ball.previous_collision = player
                return (player_group["ball"].rectangle.centery - player.rectangle.centery) / (
                    Config.PLAYER_SIZE[1]) * Config.COLLISION_STRENGTH

    @staticmethod
    def collision_with_top(game_object, change):
        min_y = 0
        if game_object.rectangle.top + change < min_y:
            game_object.rectangle.top = min_y
            return True
        return False

    @staticmethod
    def collision_with_bottom(game_object, change):
        max_y = game_display.get_height()
        if game_object.rectangle.bottom + change > max_y:
            game_object.rectangle.bottom = max_y
            return True
        return False

    def update_player(self, player, keys):
        change = 0
        if keys[0] >= 0.5:
            if not self.collision_with_top(player, -Config.PLAYER_SPEED):
                change = -Config.PLAYER_SPEED
        if keys[1] >= 0.5:
            if not self.collision_with_bottom(player, Config.PLAYER_SPEED):
                change = Config.PLAYER_SPEED
        player.rectangle.centery += change

    def update_ball(self, index):
        player_group = self.player_groups[index]
        ball = player_group["ball"]
        collision = self.collision_between_players_and_ball(player_group)
        if collision is not None:
            ball.velocity.x = -ball.velocity.x
            ball.velocity.y = collision + ball.velocity.y
        if ball.velocity.y > 0 and self.collision_with_bottom(ball, ball.velocity.y):
            ball.velocity.y = -ball.velocity.y
        elif ball.velocity.y < 0 and self.collision_with_top(ball, ball.velocity.y):
            ball.velocity.y = -ball.velocity.y
        ball.rectangle.center += ball.velocity
        if ball.rectangle.centerx > game_display.get_width() or ball.rectangle.centerx < 0:
            player_group["dead"] = True

    def render_environment(self):
        game_display.fill((0, 0, 0))
        for player_group in self.player_groups:
            for player in player_group["players"]:
                game_display.blit(*player.draw())
            game_display.blit(*player_group["ball"].draw())
        display.update()

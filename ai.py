import neat
import pygame

from game import Environment, frames_per_second

imgarray = []
xpos_end = 0


def evaluate_genomes(genomes, config):
    global environment, genomes_list, nets
    environment = Environment()
    genomes_list = []
    nets = []
    for genome_id, genome in genomes:
        environment.create_player_group()
        genomes_list.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
    while True:
        if len(environment.player_groups) == 0:
            break
        to_delete = []
        for i, player_group in enumerate(environment.player_groups):
            environment.update_ball(i)
            ball = player_group["ball"]
            fitness = 0
            for player in player_group["players"]:
                output = nets[i].activate((player.rectangle.centery, ball.rectangle.centery, abs(ball.rectangle.centerx - player.rectangle.centerx)))
                environment.update_player(player, output)
                fitness += player.score
            if player_group["dead"]:
                to_delete.append(i)
            genomes_list[i].fitness = fitness
        to_delete = to_delete[::-1]
        for key in to_delete:
            del environment.player_groups[key]
            del nets[key]
            del genomes_list[key]
        environment.render_environment()
        frames_per_second.tick(60)
        pygame.event.pump()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(evaluate_genomes, 50)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    run('config-feedforward')
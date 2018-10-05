from collections import namedtuple
from random import randrange, choice, random
from copy import deepcopy

SensorState = namedtuple('SensorState', 'terrain, sensors, coverage')


# Functions for the sensors #
def get_covered_signal_points(state: SensorState, sensor: int) -> list:
    covered = get_all_covered_points(state, sensor)
    return [(x, y) for x, y in covered if state.terrain[x][y] == 1]


def get_all_covered_points(state: SensorState, sensor: int) -> list:
    current_sensor = state.sensors[sensor]
    current_coverage = state.coverage[sensor]
    covered_points = []
    max_rows = len(state.terrain)
    max_columns = len(state.terrain[0])

    for i in range(current_coverage):
        current_row = current_sensor[0] + i
        if current_row <= max_rows - 1:
            for j in range(current_coverage):
                current_column = current_sensor[1] + j
                if current_column <= max_columns - 1:
                    covered_points.append((current_row, current_column))
    return covered_points


def get_possible_actions(state: SensorState, sensor: int) -> list:
    actions = []
    current_sensor = state.sensors[sensor]
    max_rows = len(state.terrain)
    max_columns = len(state.terrain[0])
    # Left
    if current_sensor[1] > 0:
        actions.append((current_sensor[0], current_sensor[1] - 1))

    # Right
    if current_sensor[1] < (max_columns - 1):
        actions.append((current_sensor[0], current_sensor[1] + 1))

    # Up
    if current_sensor[0] > 0:
        actions.append((current_sensor[0] - 1, current_sensor[1]))

    # Down
    if current_sensor[0] < (max_rows - 1):
        actions.append((current_sensor[0] + 1, current_sensor[1]))

    return actions


def print_coverage(state: SensorState) -> None:
    to_print = state.terrain.copy()
    to_print = [['-' if element == 1 else 'X' for element in row] for row in to_print]
    print_terrain(to_print)
    for i in range(len(state.sensors)):
        covered_points = get_all_covered_points(state, i)
        for index, tup in enumerate(covered_points):
            to_print[tup[0]][tup[1]] = '#' if to_print[tup[0]][tup[1]] == 'X' else i
    print("\n")
    print_terrain(to_print)


def print_terrain(terrain):
    print("", end="  ")
    for i in range(len(terrain[0])):
        print(i, end=" ")
    print("")
    for i in range(len(terrain)):
        print(i, end=" ")
        for j in range(len(terrain[i])):
            print(terrain[i][j], end=" ")
        print("")


# Functions for the bee algorithm #
def objective_function(state):
    coverage = set()
    for i in range(len(state.sensors)):
        coverage.update(get_covered_signal_points(state, i))
    return len(coverage)


def create_random_bee(search_space: tuple) -> dict:
    """create a random bee position"""
    positions = [(randrange(len(search_space[0])), randrange(len(search_space[0][0])))
                 for _ in range(len(search_space[1]))]
    return {'state': SensorState(terrain=search_space[0], coverage=search_space[1], sensors=positions), 'fitness': None}


def create_neigh_bee(state: SensorState, patch_size, search_space):
    """create a bee inside a neighborhood"""
    positions = deepcopy(state.sensors)
    possible_modifications = [i for i in range(len(positions))]
    for _ in range(patch_size):
        to_modify = choice(possible_modifications)
        actions = get_possible_actions(state, to_modify)
        positions[to_modify] = choice(actions)
        possible_modifications.remove(to_modify)
    return {'state': SensorState(terrain=search_space[0], coverage=search_space[1], sensors=positions), 'fitness': None}


def search_neigh(parent, neigh_size, patch_size, search_space):
    """search inside the neighborhood of a site"""
    neigh = []
    for i in range(neigh_size):
        bee = create_neigh_bee(parent['state'], patch_size, search_space)
        bee['fitness'] = objective_function(bee['state'])
        neigh.append(bee)
    neigh.sort(key=lambda b: b['fitness'], reverse=True)
    return neigh[0]


def create_scout_bees(search_space, num_scouts):
    """creates scout bees for new sites"""
    return [create_random_bee(search_space) for _ in range(num_scouts)]


def bees_algorithm(max_gens, search_space, num_bees, num_sites,
                   elite_sites, patch_size, patch_dec, e_bees, o_bees):
    """implements the Bees algorithm"""
    best = None
    pop = [create_random_bee(search_space) for _ in range(num_bees)]

    for gen in range(max_gens):
        for bee in range(num_bees):
            pop[bee]['fitness'] = objective_function(pop[bee]['state'])
        pop.sort(key=lambda b: b['fitness'], reverse=True)
        if not best or pop[0]['fitness'] > best['fitness']:
            best = pop[0]
            print("Now the best is {}".format(pop[0]['state'].sensors))
        next_gen = []
        for i, parent in enumerate(pop[:num_sites]):
            neigh_size = e_bees if i < elite_sites else o_bees
            next_gen.append(search_neigh(parent, neigh_size, patch_size,
                                         search_space))
        scouts = create_scout_bees(search_space, num_bees - num_sites)
        pop = next_gen + scouts
        if patch_dec > random():
            patch_size = patch_size - 1
        print(" > it=%d, patch_size=%g, f=%g" % (gen + 1, patch_size, best['fitness']))
    return best


# problem configuration
terr = [[1, 1, 0, 0, 1, 0],
        [1, 0, 0, 1, 1, 1],
        [0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 0]]

cov = [3, 2, 2, 1]  # domains

search_space = (terr, cov)
# algorithm configuration
max_gens = 20  # maximum number of generations
num_bees = 45  # bees working
num_sites = 3  #
elite_sites = 1
patch_size = 3
patch_dec = 0.05  # decrease of patch size in each generation
e_bees = 7  # number of elite bees
o_bees = 2  # number of other bees
# execute the algorithm
result = bees_algorithm(max_gens, search_space, num_bees, num_sites,
                        elite_sites, patch_size, patch_dec, e_bees, o_bees)

print("Best result is {} with value of {}".format(result["state"].sensors, result["fitness"]))
print_coverage(result["state"])

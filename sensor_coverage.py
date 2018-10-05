from search import *
from collections import namedtuple

SensorState = namedtuple('SensorState', 'terrain, sensors, coverage')


class Sensor(Problem):

    def __init__(self, initial, goal=None):
        super().__init__(initial, goal)
        self.initial = initial
        self.goal = goal
        self.maxRows = len(initial.terrain)
        self.maxColumns = len(initial.terrain[0])

    def actions(self, state: SensorState):
        actions = []
        for i in range(len(state.sensors)):
            actions += self.get_actions(state, i)
        return actions

    def get_actions(self, state: SensorState, sensor: int) -> list:
        actions = []
        current_sensor = state.sensors[sensor]

        # Left
        if current_sensor[1] > 0:
            actions.append((sensor, current_sensor[0], current_sensor[1] - 1))

        # Right
        if current_sensor[1] < (self.maxColumns - 1):
            actions.append((sensor, current_sensor[0], current_sensor[1] + 1))

        # Up
        if current_sensor[0] > 0:
            actions.append((sensor, current_sensor[0] - 1, current_sensor[1]))

        # Down
        if current_sensor[0] < (self.maxRows - 1):
            actions.append((sensor, current_sensor[0] + 1, current_sensor[1]))

        return actions

    def result(self, state: SensorState, action: list) -> SensorState:
        result = state.sensors.copy()
        result[action[0]] = (action[1], action[2])
        return SensorState(terrain=state.terrain, sensors=result, coverage=state.coverage)

    def value(self, state: SensorState) -> int:
        coverage = set()
        for i in range(len(state.sensors)):
            coverage.update(self.get_covered_signal_points(state, i))
        return len(coverage)

    def get_covered_signal_points(self, state: SensorState, sensor: int) -> list:
        covered = self.get_all_covered_points(state, sensor)
        return [(x, y) for x, y in covered if state.terrain[x][y] == 1]

    def get_all_covered_points(self, state: SensorState, sensor: int) -> list:
        current_sensor = state.sensors[sensor]
        current_coverage = state.coverage[sensor]
        covered_points = []
        for i in range(current_coverage):
            current_row = current_sensor[0] + i
            if current_row <= self.maxRows - 1:
                for j in range(current_coverage):
                    current_column = current_sensor[1] + j
                    if current_column <= self.maxColumns - 1:
                        covered_points.append((current_row, current_column))
        return covered_points

    def print_coverage(self, state: SensorState) -> None:
        to_print = state.terrain.copy()
        to_print = [['-' if element == 1 else 'X' for element in row] for row in to_print]
        self.print_terrain(to_print)
        for i in range(len(state.sensors)):
            covered_points = self.get_all_covered_points(state, i)
            for index, tup in enumerate(covered_points):
                to_print[tup[0]][tup[1]] = '#' if to_print[tup[0]][tup[1]] == 'X' else i
        print("\n")
        self.print_terrain(to_print)

    @staticmethod
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


ter = [[1, 1, 0, 0, 1, 0],
       [1, 0, 0, 1, 1, 1],
       [0, 0, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1],
       [0, 0, 0, 1, 1, 1],
       [1, 1, 1, 1, 0, 0]]
sens = [(0, 0), (0, 4), (3, 4), (4, 2)]
cov = [3, 2, 2, 1]

initialState = SensorState(terrain=ter, sensors=sens, coverage=cov)
testProblem = Sensor(initialState)
res = simulated_annealing(testProblem, exp_schedule(k=100, limit=2000))
print("Sensors positions -> {}".format(res.state.sensors))
print("Result -> {} covered".format(testProblem.value(res.state)))

testProblem.print_coverage(res.state)

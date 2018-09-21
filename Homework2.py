from search import Problem, depth_first_graph_search, breadth_first_search
from copy import deepcopy


class CleanUpPuzzle(Problem):

    def __init__(self, initial, goal=None):
        super().__init__(initial, goal)

    def actions(self, state):
        """Return the actions that can be executed in the given state."""
        possible_states = set()
        for x, y in state.points:
            for possibility in state.get_adjacent_nodes(x, y):
                possible_states.add(possibility)
        return possible_states

    def result(self, state, action):
        """Return the state that results from executing the given action in the given state."""
        new_state = deepcopy(state)
        x, y = action
        new_state.push(x, y)
        return new_state

    def goal_test(self, state):
        """Return True if the state is a goal."""
        return state.points == self.goal.points

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from state1 via action, assuming cost c to get
        up to state1."""
        # TODO
        pass

    def value(self, state):
        pass


class PuzzleState:

    def __init__(self, size=11, points=None) -> None:
        self.size = size
        self.points = points

    def __str__(self) -> str:
        acc = "\n"
        for row in range(self.size):
            acc += ("-" * (self.size * 2 + 1)) + "\n"
            for column in range(self.size):
                if (column, row) in self.points:
                    label = "0"
                else:
                    label = "-"
                acc += "|{}".format(label)

            acc += "|\n"
        acc += ("-" * (self.size * 2 + 1)) + "\n"
        return acc

    def print_board(self):
        for row in range(self.size):
            print("-" * (self.size * 2 + 1))
            for column in range(self.size):
                if (column, row) in self.points:
                    label = "0"
                else:
                    label = "-"
                print("|{}".format(label), end="")

            print("|")
        print("-" * (self.size * 2 + 1))

    def get_adjacent_nodes(self, x, y) -> list:
        result = []
        if x > 0:
            result.append((x - 1, y))
        if x < self.size - 1:
            result.append((x + 1, y))
        if y > 0:
            result.append((x, y - 1))
        if y < self.size - 1:
            result.append((x, y + 1))
        return result

    def push(self, x, y):
        adjacent_points = self.get_adjacent_nodes(x, y)
        for point in adjacent_points:
            if point in self.points:
                self.points.remove(point)
            else:
                self.points.append(point)


def print_solution(result):
    print("Initial board is: {}".format(result.path()[0].state))
    print("The sequence is:")
    for action in result.solution():
        print("Push tile {}".format(action))
    print("Resultant board is: {}".format(result.state))


initial_state = PuzzleState(points=[(0, 1), (1, 0), (9, 10), (10, 9), (5, 4), (5, 6), (4, 5), (6, 5)])

goal = PuzzleState(points=[])

puzzle = CleanUpPuzzle(initial_state, goal=goal)

result = breadth_first_search(puzzle)
if result:
    print_solution(result)


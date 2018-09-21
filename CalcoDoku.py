from csp import CSP, backtracking_search, count


class CalcoDoku(CSP):
    def __init__(self, size, groups, operation):
        self.operation = operation
        self.size = size

        variables = ["{},{}".format(j, i) for j in range(size) for i in range(size)]
        domains = {i: [x for x in range(1, size + 1)] for i in variables}
        self.groups = groups
        neighbors = {item: [x for x in group.items if x != item] for group in groups for item in group.items}

        super().__init__(variables, domains, neighbors, self.constraint)

    def constraint(self, position_a, a, _, b):
        # print("({}) = {},({}) = {}".format(position_a, a, position_b, b))
        group_result, = [group.goal for group in self.groups if position_a in group.items]

        if self.operation == "+":
            return a + b == group_result
        elif self.operation == "-":
            return a - b == group_result or b - a == group_result
        elif self.operation == "*":
            return a * b == group_result
        elif self.operation == "/":
            return a / b == group_result

    def nconflicts(self, var, val, assignment):
        # print(assignment)
        x, y = var.split(",")
        acc = 0
        for i in assignment.keys():
            x2, y2 = i.split(",")
            if (x == x2 and y != y2) or (x != x2 and y == y2):
                if val == assignment[i]:
                    acc += 1

        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))

        if not self.neighbors[var]:
            group_result, = [group.goal for group in self.groups if var in group.items]
            if group_result != val:
                return acc + 1

        return acc + count(conflict(v) for v in self.neighbors[var])

    def display(self, assignment):
        for i in range(self.size):
            for j in range(self.size):
                print("|{}".format(assignment["{},{}".format(j, i)]), end="")
            print("|")


class Group:
    def __init__(self, goal, items):
        self.goal = goal
        self.items = items


groups = [Group(3, ["0,0", "0,1"]),
          Group(7, ["1,0", "1,1"]),
          Group(6, ["2,0", "3,0"]),
          Group(6, ["0,2", "1,2"]),
          Group(4, ["0,3", "1,3"]),
          Group(4, ["3,1", "3,2"]),
          Group(5, ["2,2", "2,3"]),
          Group(1, ["2,1"]),
          Group(4, ["3,3"])]

calco = CalcoDoku(4, groups, "+")
result = backtracking_search(calco)
calco.display(result)

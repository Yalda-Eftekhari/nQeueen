import random

def input_board_size():
    n = input("Enter an integer for the size of the board: ")
    return int(n)


class NQueens:
    def __init__(self, n):
        self.queens_position = self.generate_random_board(n)
        self.n = n

    def generate_random_board(self, n):
        queens_position = []

        for i in range(n):
            random_number = random.randint(0, n - 1)
            queens_position.append((i, random_number))
        return queens_position

    def print_board(self, positions):
        board = [[0] * self.n for _ in range(self.n)]
        for pos in positions:
            board[pos[0]][pos[1]] = 1

        print('Board:')
        for i in range(len(board)):
            print(str(board[i]) + ' ', end='')
            print()

        print('Heuristic value: ', self.determine_heuristic_cost(positions))
        print()

    def determine_heuristic_cost(self, queens_position):
        return sum((self.conflicts_for_specific_queen(pos, queens_position)) for pos in queens_position)

    def coloumn_under_attack(self, pos, current_positions):
        res = 0
        for queen in current_positions:
            if pos[1] == queen[1] and queen != pos:
                res += 1
        return res

    def row_under_attack(self, pos, current_positions):
        res = 0
        for queen in current_positions:
            if pos[0] == queen[0] and queen != pos:
                res += 1
        return res

    def diagonal_under_attack(self, pos, current_positions):
        res = 0
        for queen in current_positions:
            if (abs(queen[0] - pos[0]) == abs(queen[1] - pos[1]) and queen != pos):
                res += 1
        return res

    def conflicts_for_specific_queen(self, position, current_positions):  # for first heuristic
        return self.coloumn_under_attack(position, current_positions) + \
               self.row_under_attack(position, current_positions) + \
               self.diagonal_under_attack(position, current_positions)

    # def conflicts_for_specific_queen(self, position, current_positions):  # for second heuristic
    #     res = self.coloumn_under_attack(position, current_positions) + \
    #            self.diagonal_under_attack(position, current_positions)
    #     return 0 if res == 0 else 1

    def find_child(self, current_positions, n=8, random_choice=False):
        child = []
        current_h_cost = self.determine_heuristic_cost(current_positions)
        same_cost_children = []

        for row in range(n):
            for col in range(n):
                temp_position = current_positions.copy()
                temp_position[row] = (row, col)
                temp_h_cost = self.determine_heuristic_cost(temp_position)
                if (random_choice):
                    if temp_position != current_positions:
                        if temp_h_cost < current_h_cost:
                            child = temp_position.copy()
                            current_h_cost = temp_h_cost
                        elif temp_h_cost == current_h_cost:
                            same_cost_children.append(temp_position)
                            x = random.randint(0, len(same_cost_children) - 1)
                            child = same_cost_children[x]
                else:
                    if (temp_position != current_positions) and (temp_h_cost < current_h_cost):
                        child = temp_position.copy()
                        current_h_cost = temp_h_cost
        return child


def nqueens_solver_by_conflict_minimizing_and_restart(max_iterations=14000):
    number_of_iterations = 0
    number_of_restarts = 0
    board_size = input_board_size()
    obj = NQueens(board_size)
    current_positions = obj.queens_position.copy()

    obj.print_board(current_positions)

    for _ in range(max_iterations):
        next_node = obj.find_child(current_positions, board_size).copy()

        if len(next_node) != 0:
            obj.print_board(next_node)

        number_of_iterations += 1
        if len(next_node) == 0:
            print('failed')
            print('----------------------------------------')
            next_node = obj.generate_random_board(board_size)
            obj.queens_position = next_node.copy()
            number_of_restarts += 1

        if obj.determine_heuristic_cost(next_node) == 0:
            print('success')
            break

        current_positions = next_node.copy()

    print("Steps taken: ", number_of_iterations)
    print("Restarts: ", number_of_restarts)


if __name__ == "__main__":
    nqueens_solver_by_conflict_minimizing_and_restart()
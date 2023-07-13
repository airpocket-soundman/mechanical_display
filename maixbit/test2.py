import time
import random


lista = [[1,1],[1,1]]

total_sum = sum(element for row in lista for element in row)
print(total_sum)

def initialize_board(ini = "glider"):
    # 初期状態の盤面を生成する
    board = [[0] * 16 for _ in range(16)]
    print(ini)
    # 盤面の一部を初期配置として設定する

    if ini == "glider":
        board[5][6] = 1
        board[6][7] = 1
        board[7][5] = 1
        board[7][6] = 1
        board[7][7] = 1
    
    else:
        positions = random.sample(range(256), ini)
        for pos in positions:
            row = pos // 16
            col = pos % 16
            board[row][col] = 1

    return board


def print_board(board):
    # 盤面を表示する
    for row in board:
        for cell in row:
            if cell == 0:
                print(".", end=" ")
            else:
                print("O", end=" ")
        print()
    print()

def count_neighbors(board, row, col):
    # 指定されたセルの周囲の生存セルの数を数える
    count = 0
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if (i, j) != (row, col):
                # 周期境界条件を適用する
                neighbor_row = (i + 16) % 16
                neighbor_col = (j + 16) % 16
                count += board[neighbor_row][neighbor_col]
    return count

def update_board(board):
    # 盤面を更新する
    new_board = [[0] * 16 for _ in range(16)]
    
    for i in range(16):
        for j in range(16):
            count = count_neighbors(board, i, j)
            if board[i][j] == 1 and (count == 2 or count == 3):
                new_board[i][j] = 1
            elif board[i][j] == 0 and count == 3:
                new_board[i][j] = 1
    
    return new_board

def run_life_game():
    # Life Gameを実行する
    life_num = 20
    board = initialize_board(20)
    print("Initial state:")
    print_board(board)


    for generation in range(500):
        board = update_board(board)
        total_life = sum(element for row in board for element in row)
        print(total_life)
        if total_life == 0:
            board = initialize_board(life_num)
        if generation%10 == 0:
            board[random.randint(0, 15)][random.randint(0, 15)] = 1
        print(f"Generation {generation+1}:")
        print_board(board)
        time.sleep(0.2)
run_life_game()
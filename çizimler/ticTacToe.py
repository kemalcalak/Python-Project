board = [[" " for x in range(10)] for y in range(10)]
player = "X"

def print_board():
    print("  | 0 1 2 3 4 5 6 7 8 9")
    print("--|------------------")
    for i in range(10):
        print(str(i) + " | " + " ".join(board[i]))

def make_move():
    global player
    row = int(input("Enter row number: "))
    col = int(input("Enter column number: "))
    if board[row][col] == " ":
        board[row][col] = player
        if player == "X":
            player = "O"
        else:
            player = "X"
    else:
        print("That spot is already taken!")

def check_win():
    for i in range(10):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return True
        elif board[0][i] == board[1][i] == board[2][i] != " ":
            return True
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return True
    elif board[0][2] == board[1][1] == board[2][0] != " ":
        return True
    else:
        return False

print("Welcome to Tic Tac Toe!")
print_board()

while not check_win():
    make_move()
    print_board()

print("Game over! " + player + " wins!")
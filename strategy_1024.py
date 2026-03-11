def strategy(board):
    # helper to check possible merge in a row or column
    def can_merge(lst):
        for i in range(len(lst)-1):
            if lst[i] > 0 and lst[i] == lst[i+1]:
                return True
        return False

    # try to move in a direction that creates a merge
    for dir, delta in [("W", (-1,0)), ("A", (0,-1)), ("S", (1,0)), ("D", (0,1))]:
        merged = False
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] > 0:
                    ni, nj = i + delta[0], j + delta[1]
                    if 0 <= ni < len(board) and 0 <= nj < len(board[0]):
                        if board[ni][nj] == 0:
                            return dir
                        if board[ni][nj] == board[i][j]:
                            return dir
    # fallback: move down
    return "S"
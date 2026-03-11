def strategy(board):
    # board is a 4x4 list of lists
    import random
    
    # Directions with priority: diagonal corners
    dirs = ['W', 'A', 'S', 'D']
    for d in dirs:
        new_board = [row[:] for row in board]
        if d == 'W':
            for j in range(4):
                merged = False
                for i in range(1, 4):
                    if new_board[i][j] == new_board[i-1][j] and not merged:
                        new_board[i-1][j] += new_board[i][j]
                        new_board[i][j] = 0
                        merged = True
        elif d == 'S':
            for j in range(4):
                merged = False
                for i in range(2, -1, -1):
                    if new_board[i][j] == new_board[i+1][j] and not merged:
                        new_board[i+1][j] += new_board[i][j]
                        new_board[i][j] = 0
                        merged = True
        elif d == 'A':
            for i in range(4):
                merged = False
                for j in range(1, 4):
                    if new_board[i][j] == new_board[i][j-1] and not merged:
                        new_board[i][j-1] += new_board[i][j]
                        new_board[i][j] = 0
                        merged = True
        elif d == 'D':
            for i in range(4):
                merged = False
                for j in range(2, -1, -1):
                    if new_board[i][j] == new_board[i][j+1] and not merged:
                        new_board[i][j+1] += new_board[i][j]
                        new_board[i][j] = 0
                        merged = True
        # measure score: number of non-zero tiles
        score = sum(1 for r in new_board for v in r if v != 0)
        # choose first direction that reduces empty tiles
        if score > sum(1 for r in board for v in r if v != 0):
            return d
    return random.choice(dirs)
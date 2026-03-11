def strategy(board):
    size = len(board)
    # Helper to compute score of moves
    def score_move(d):
        new_board = [row[:] for row in board]
        moved = False
        if d == "W":
            for j in range(size):
                col = [new_board[i][j] for i in range(size)]
                merged = merge(col)
                for i in range(size):
                    new_board[i][j] = merged[i]
                if merged != col:
                    moved = True
        elif d == "S":
            for j in range(size):
                col = [new_board[i][j] for i in range(size)][::-1]
                merged = merge(col)[::-1]
                for i in range(size):
                    new_board[i][j] = merged[i]
                if merged[::-1] != col:
                    moved = True
        elif d == "A":
            for i in range(size):
                row = new_board[i][:]
                merged = merge(row)
                new_board[i] = merged
                if merged != row:
                    moved = True
        elif d == "D":
            for i in range(size):
                row = new_board[i][::-1]
                merged = merge(row)[::-1]
                new_board[i] = merged
                if merged[::-1] != row:
                    moved = True
        return moved, new_board

    def merge(line):
        filtered = [x for x in line if x != 0]
        merged = []
        i = 0
        while i < len(filtered):
            if i+1 < len(filtered) and filtered[i] == filtered[i+1]:
                merged.append(filtered[i]*2)
                i += 2
            else:
                merged.append(filtered[i])
                i += 1
        merged += [0]*(size-len(merged))
        return merged

    # Evaluate each direction
    best_score = -1
    best_dir = "W"
    for d in "WASD":
        moved, new_board = score_move(d)
        if not moved:
            continue
        # simple heuristic: sum of all tiles
        score = sum(sum(row) for row in new_board)
        if score > best_score:
            best_score = score
            best_dir = d
    return best_dir
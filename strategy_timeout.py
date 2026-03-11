def strategy(board):
    # Prioritize merges, then favor left/up moves
    rows, cols = len(board), len(board[0]) if board else 0

    # Helper to check if a move is possible
    def can_move(direction):
        if direction == 'W':
            for c in range(cols):
                for r in range(rows-1):
                    if board[r][c] == 0 or board[r][c] == board[r+1][c]:
                        return True
        elif direction == 'A':
            for r in range(rows):
                for c in range(cols-1):
                    if board[r][c] == 0 or board[r][c] == board[r][c+1]:
                        return True
        elif direction == 'S':
            for c in range(cols):
                for r in range(rows-1,0,-1):
                    if board[r][c] == 0 or board[r][c] == board[r-1][c]:
                        return True
        elif direction == 'D':
            for r in range(rows):
                for c in range(cols-1,0,-1):
                    if board[r][c] == 0 or board[r][c] == board[r][c-1]:
                        return True
        return False

    # Generate all moves
    moves = []
    for d in ['W', 'A', 'S', 'D']:
        if can_move(d):
            moves.append(d)

    # If multiple moves, pick one that maximizes the sum of merges
    if not moves:
        return 'W'  # fallback
    # Simple heuristic: prefer first move that allows a merge
    return moves[0]
def strategy(board):
    import random, copy

    def rotate(b):
        return [[b[3-j][i] for j in range(4)] for i in range(4)]

    def compress(b):
        new = []
        for row in b:
            new_row = [x for x in row if x != 0]
            new_row += [0]*(4-len(new_row))
            new.append(new_row)
        return new

    def merge(b):
        for row in b:
            for i in range(3):
                if row[i]==row[i+1] and row[i]!=0:
                    row[i]*=2
                    row[i+1]=0

    def move(b, dir):
        if dir=="W":
            return merge(rotate(compress(rotate(b))))
        if dir=="S":
            return rotate(merge(compress(rotate(b))))
        if dir=="A":
            return merge(compress(b))
        if dir=="D":
            return rotate(merge(compress(rotate(b))))  # actually reverse

    best_score=0
    best_move=None
    for move_dir in "WASD":
        new_board=move(copy.deepcopy(board), move_dir)
        score=sum(sum(row) for row in new_board)
        if score>best_score:
            best_score=score
            best_move=move_dir
    return best_move
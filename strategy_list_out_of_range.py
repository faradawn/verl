def strategy(board):
    # helper to rotate board
    def rotate(b): return [list(col)[::-1] for col in zip(*b)]
    # helper to move up
    def move_up(b):
        n=len(b)
        new=[[] for _ in range(n)]
        for j in range(n):
            col=[b[i][j] for i in range(n) if b[i][j]!=0]
            merged=[]
            i=0
            while i< len(col):
                if i+1<len(col) and col[i]==col[i+1]:
                    merged.append(col[i]*2)
                    i+=2
                else:
                    merged.append(col[i])
                    i+=1
            new_col=[0]*(n-len(merged))+merged
            for i in range(n):
                new[i][j]=new_col[i]
        return new
    best=None
    best_val=-1
    for dir in ["W","A","S","D"]:
        # move board in given direction
        b=[row[:] for row in board]
        if dir=="W": b=move_up(b)
        elif dir=="S": b=[list(row[::-1]) for row in move_up([row[::-1] for row in b])]
        elif dir=="A": b=[list(row[::-1]) for row in move_up([row[::-1] for row in b])]
        elif dir=="D": b=[list(row[::-1]) for row in b]
        # evaluate
        val=max(max(row) for row in b)
        if val>best_val:
            best_val=val; best=dir
    return best
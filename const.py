def globs(size):
    # Input: Size string 's' small or 'l' large
    # Output: D, V, M, k, gamma
    if size == 's':
        return 8, 12, 10, 5, 0.2
    elif size == 'l':
        return 100, 18, 5, 6, 0.2
    else:
        print('Size not valid, choose either s or l')
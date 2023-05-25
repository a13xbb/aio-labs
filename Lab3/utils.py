def weights_dp(cap: int, p: list, w: list):
    '''DP on weights'''
    n = len(w)
    dp = [[0 for i in range(cap + 1)] for i in range(n + 1)]
    items = []
    for i in range(1, n + 1):
        for j in range(1, cap + 1):
            wi = w[i - 1]
            if wi <= j:
                dp[i][j] = max(dp[i - 1][j], p[i - 1] + dp[i - 1][j - wi])
            else:
                dp[i][j] = dp[i - 1][j]
                
    def findAns(dp: list, i: int, j: int, w: list):
        if dp[i][j] == 0: 
            return
        if dp[i - 1][j] == dp[i][j]:
            findAns(dp, i - 1, j, w)
        else:
            findAns(dp, i - 1, j - w[i - 1], w)
            items.append(i - 1)
            
    findAns(dp, n, cap, w)        
    indexes = []
    for i in range(n):
        if i in items:
            indexes.append(1)
        else:
            indexes.append(0)
    
    return indexes, dp[n][cap]


def count_profit(items: list, p: list):
    profit = 0
    for i, item in enumerate(items):
        profit += item * p[i]
    
    return profit


def count_weights(items: list, w: list):
    weight = 0
    for i, item in enumerate(items):
        weight += item * w[i]
    
    return weight


def upper_bound(arr: list, target: int):
    for i, item in enumerate(arr):
        if item > target:
            return i
            
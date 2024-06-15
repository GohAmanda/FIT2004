
from cmath import inf
# Bottom up
def coin (coin):
    memo = [inf] *(N+1) # initialize memory N+1 because want to including 0 --> I want 0 to 12
    memo[0] = 0 # initiate Base
    for value in range (1, N+1): # loop memo and fill it up
        for j in range (M): # go through the coins
            if coin[j] <= value: 
                balance = value - coin[j]
                count = 1 + memo[balance]
                if count < memo[value]: # if we have new optimal
                    memo[value]=count
                    
    #return memo[N]
    print(memo)
class Items:

    def __init__(self, weight, value):
        self.weight = weight
        self.profit = value

def bagWeight (items):
    memo = [0] *(N+1) # initialize memory N+1 because want to including 0 --> I want 0 to 12
    memo[0] = 0 # initiate Base
    for bag_weight in range (1, N+1): # loop memo and fill it up
        for j in range (M): # go through the coins
            if items[j].weight <= bag_weight: 
                balance = bag_weight - items[j].weight
                profit = items[j].profit + memo[balance]
                if profit > memo[bag_weight]: # if we have new optimal
                    memo[bag_weight]=profit
                    
    #return memo[N]
    print(memo)

# Another method for the bagWeight method (this is in matrix form)
# for i=1 to M:
#     for j=1 to N:
#     exclude = memo[i-1][j]
#     include = 0
#     if item[i].weight <= j:
#         include =item[i].value + memo[i-1][j-item[i].weight]
#     memo[i][j] = max(exclude, include)

if __name__ == "__main__":
    coins = [1,5,6,9]
    N = 12
    M = len(coins)
    coin(coins)

#Something wrong withe output here!!!!!!! Lect 06
    items = [
        Items(weight=9, value=550), Items(weight=5,value=350),Items(weight=6, value=1800), Items(weight=1,value=40)
    ]
    N=12
    M=len(items)
    bagWeight(items)

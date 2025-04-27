from typing import List, Dict

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Finds the optimal way to cut the rod using memoization.

    Args:
        length: length of the rod
        prices: list of prices, where prices[i] is the price of a rod of length i+1

    Returns:
        Dict with the maximum profit and the list of cuts
    """
    # Memoization
    memo = [-1] * (length + 1)  # Array to store results
    cuts = [-1] * (length + 1)  # Array to record cuts
    
    def helper(n: int) -> int:
        if n == 0:
            return 0
        if memo[n] != -1:
            return memo[n]
        
        max_profit = -float('inf')
        for i in range(1, n + 1):
            profit = prices[i - 1] + helper(n - i)
            if profit > max_profit:
                max_profit = profit
                cuts[n] = i
        
        memo[n] = max_profit
        return max_profit

    # Find the maximum profit
    max_profit = helper(length)
    
    # Determine the cuts
    cuts_list = []
    remaining_length = length
    while remaining_length > 0:
        cuts_list.append(cuts[remaining_length])
        remaining_length -= cuts[remaining_length]

    return {
        "max_profit": max_profit,
        "cuts": cuts_list,
        "number_of_cuts": len(cuts_list) - 1
    }

def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Finds the optimal way to cut the rod using tabulation.

    Args:
        length: length of the rod
        prices: list of prices, where prices[i] is the price of a rod of length i+1

    Returns:
        Dict with the maximum profit and the list of cuts
    """
    # Tabulation
    dp = [0] * (length + 1)
    cuts = [-1] * (length + 1)
    
    for n in range(1, length + 1):
        max_profit = -float('inf')
        for i in range(1, n + 1):
            profit = prices[i - 1] + dp[n - i]
            if profit > max_profit:
                max_profit = profit
                cuts[n] = i
        dp[n] = max_profit

    # Determine the cuts
    cuts_list = []
    remaining_length = length
    while remaining_length > 0:
        cuts_list.append(cuts[remaining_length])
        remaining_length -= cuts[remaining_length]

    return {
        "max_profit": dp[length],
        "cuts": cuts_list,
        "number_of_cuts": len(cuts_list) - 1
    }

def run_tests():
    """Function to run all tests."""
    test_cases = [
        # Test 1: Basic case
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Basic case"
        },
        # Test 2: Optimal not to cut
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Optimal not to cut"
        },
        # Test 3: All cuts of length 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Uniform cuts"
        }
    ]

    for test in test_cases:
        print(f"\nTest: {test['name']}")
        print(f"Rod length: {test['length']}")
        print(f"Prices: {test['prices']}")

        # Test memoization
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nMemoization result:")
        print(f"Maximum profit: {memo_result['max_profit']}")
        print(f"Cuts: {memo_result['cuts']}")
        print(f"Number of cuts: {memo_result['number_of_cuts']}")

        # Test tabulation
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nTabulation result:")
        print(f"Maximum profit: {table_result['max_profit']}")
        print(f"Cuts: {table_result['cuts']}")
        print(f"Number of cuts: {table_result['number_of_cuts']}")

        print("\nTest passed successfully!")

if __name__ == "__main__":
    run_tests()
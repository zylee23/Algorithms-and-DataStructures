"""
Name: Lee Zi Yan
Student ID: 31264689
"""

#Question 1
#%%
def best_schedule(weekly_income, competitions):
    """
    Get the maximum amount of money that can be earned by combining the earnings
    from weekly_income and competitions
    :param weekly_income: a list of non-negative integers, where weekly_income[i]
                          is the amount of money earned working in week i
    :param competitions: a list of tuples, aach tuple contains 3 non-negative integers,
                         (start_time, end_time, winnings)
                         - from start_time to end_time, no working
                         - winnings is the money earned if compete
    :return: the maximum amount of money that can be earned
    :best time complexity: O(NlogN), N is the total number of elements in weekly_income and competitions put together
    :worst time complexity: O(NlogN)
    :aux space complexity: O(N)
    """
    # initialise memoisation array
    memo = [0] * (len(weekly_income)+1)
    # change element in weekly_income to follow competitions, (start_time, end_time, winnings)
    for i in range(len(weekly_income)):
        weekly_income[i] = (i, i, weekly_income[i])
    # add element in competitions if end_time is no later than last week of weekly_income
    for j in range(len(competitions)):
        if competitions[j][1] < len(weekly_income):
            weekly_income.append(competitions[j])
    # sort according to end_time
    weekly_income.sort(key = end_time)
    # if money earned from start_time to end_time plus start_time-1 is
    # more than current money at end_time
    for k in range(len(weekly_income)):
        earn = memo[weekly_income[k][0]] + weekly_income[k][2]
        if earn > memo[weekly_income[k][1]+1]:
            memo[weekly_income[k][1]+1] = earn
    # return money earned at last day
    return memo[-1]

def end_time(elem):
    """
    Returns the second item (index = 1) from a tuple with 3 items
    :param elem: a tuple with 3 items
    :return: the first item or item at index = 1
    :best time complexity: O(1)
    :worst time complexity: O(1)
    :aux space complexity: O(1)
    """
    return elem[1]


#Question 2
# %%
def best_itinerary(profit, quarantine_time, home):
    """
    - Get the maximum amount of money that can be earned by a travelling salesman.
    - There are n cities and salesman knows how much can be earned at which city on which day
    - Salesman can either work at current city or travel.
    - Salesman can travel to either the left city or right city, which takes 1 day.
    - If salesman decided to travel to another city and stay, has to quarantine due to Covid-19.
    :param profit: a list of lists of length n
                   - each interior list represents a different day
                   - profit[d][c] is the profit that the saleman will make by working in city c on day d.
    :param quarantine_time: a list of non-negative integers, quarantine_time[i] is the number of
                            days city i requires visitors to quarantine before they can work there
    :param home: integer between 0 and n-1 inclusive, which represents the city that the salesman starts in
    :return: the maximum amount of money that can be earned by the salesman
    :best time complexity: O(nd), n is the number of cities, d is the number of days(no of interior lists in profit)
    :worst time complexity: O(nd)
    :aux space complexity: O(nd)
    """
    # initialise two memoisation arrays
    #cont records the profit earned by passing through cities instead of staying and quarantine
    memo, cont = [], []
    for _ in range(len(profit)+1):
        memo.append([0] * len(quarantine_time))
        cont.append([0] * len(quarantine_time))

    def _pass_through(day, city):
        """
        Gets the the maximum earnings for the remaining days from either passing through
        the left or right cities if salesman is at a certain city on a certain day
        - by copying from lower-left or lower-right diagonal position in cont
        :param day: the current day
        :param city: the current city
        :return: the maximum earnings from either passing through the left or right for the remaining days
        :best time complexity: O(1)
        :worst time complexity: O(1)
        :aux space complexity: O(1)
        """
        # if there is only one city, no adjacent city
        if len(quarantine_time) == 1:
            cont[day][city] = 0
        # if at leftmost city, copy lower-right diagonal
        elif city == 0:
            cont[day][city] = cont[day+1][city+1]
        # if at rightmost city, copy lower-left diagonal
        elif city == len(quarantine_time)-1:
            cont[day][city] = cont[day+1][city-1]
        else:
            # if there are cities at both sides, copy the larger value
            cont[day][city] = max(cont[day+1][city+1], cont[day+1][city-1])
        return cont[day][city]

    def _get_left(day, city):
        """
        Calculate the money earned for the remaining days if travel to city at the left and quarantine
        :param day: the current day
        :param city: the current city
        :return: the money earned for the remaining days if travel to left city and stay
        :best time complexity: O(1)
        :worst time complexity: O(1)
        :aux space complexity: O(1)
        """
        left = city-1
        # if leftmost city or the time to quarantine exceeds the number of days from current day
        if left < 0 or day+quarantine_time[left]+1 >= len(memo)-1:
            return 0
        else:
            ret = memo[day+quarantine_time[left]+1][left]
            # if money earned from travelling to left and quarantine is more than passing through
            if ret > cont[day][city]:
                cont[day][city] = ret
            return ret

    def _get_right(day, city):
        """
        Calculate the money earned for the remaining days if travel to city at the right and quarantine
        :param day: the current day
        :param city: the current city
        :return: the money earned for the remaining days if travel to right city and stay
        :best time complexity: O(1)
        :worst time complexity: O(1)
        :aux space complexity: O(1)
        """
        right = city+1
        # if rightmost city or the time to quarantine exceeds the number of days from current day
        if right > len(quarantine_time)-1 or day+quarantine_time[right]+1 >= len(memo)-1:
            return 0
        else:
            ret = memo[day+quarantine_time[right]+1][right]
            # if money earned from travelling to right and quarantine is more than passing through
            if ret > cont[day][city]:
                cont[day][city] = ret
            return ret

    # iterate from last day to first day
    for i in range(len(profit)-1, -1, -1):
        for j in range(len(quarantine_time)):
            pas = _pass_through(i, j)
            left = _get_left(i, j)
            right = _get_right(i, j)
            # if continue to stay at current city and work
            work = profit[i][j] + memo[i+1][j]

            earn = max(pas, left, right, work)
            if left == earn:
                memo[i][j], cont[i][j] = left, left
            elif right == earn:
                memo[i][j], cont[i][j] = right, right
            elif work == earn:
                memo[i][j] = work
            else:
                memo[i][j] = pas

    return memo[0][home]

#%%

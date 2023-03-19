"""
Name: Lee Zi Yan
Student ID: 31264689
"""

########## Question 1 ##########
#%%
def numOfDigits(n):
    """
    Counts the number of digits of a positive integer
    :param n: the integer to be processed
    :return: number of digits of n
    :best time complexity: O(1)
    :worst time complexity: O(k), k is the number of digits of n
    :aux space complexity: O(1)
    """
    count = 0
    while n > 0:
        count += 1
        n //= 10
    return count

#%%
def counting_sort(lst, exp):
    """
    Sorts the integers in the list in a stable manner according to the k-th least
    significant digit which is determined by the parameter exp
    :param lst: list of integers
    :param exp: column of digit from the right to be compared
    :return: sorted list based on the k-th least significant digit in non-decreasing order
    :best time complexity: O(N+M), N is the number of elements in lst
                                   M is the number of unique non-negative integers of the base
    :worst time complexity: O(N+M)
    :aux space complexity: O(N+M)
    """
    base = 10
    # initialise count array
    count_arr = [None] * base
    for i in range(len(count_arr)):
        count_arr[i] = []
    # update count array
    for item in lst:
        col = item//(base**exp)%10
        count_arr[col].append(item)
    # update lst by putting each element at the correct index
    index = 0
    for j in range(len(count_arr)):
        for k in range(len(count_arr[j])):
            lst[index] = count_arr[j][k]
            index += 1
    return lst

#%%
def radix_sort(lst):
    """
    Sorts a list of integers, column by column from the least significant digit to the
    most significant digit in a non-decreasing manner
    :param lst: list of integers
    :return: sorted list of integers in non-decreasing order
    :best time complexity: O(1)
    :worst time complexity: O(kN), k is the greatest number of digits in any element
                                   N is the number of elements in lst
    :aux space complexity: O(N+M), M is the number of unique non-negative integers of the base
                                   in counting_sort(lst, exp)
    """
    # empty list or list with one element is already sorted
    if len(lst) <= 1:
        return lst
    # find number of digits of the greatest integer
    max_item = max(lst)
    max_column = numOfDigits(max_item)
    # counting sort for numbers in each col
    # going from right to left
    for i in range(max_column):
        counting_sort(lst, i)
    return lst

#%%
def best_interval(transactions, t):
    """
    Determines the interval of a given length, t that contains the most transactions
    from a large dataset of transaction records
    :param transactions: unsorted list of non-negative integers, where each integer
                         represents the time that some transaction occurred
    :param t: non-negative integer, representing a length of time in seconds
    :return: two element tuple, (best_t, count)
                best_t is the minimal start time of interval with length t with the most transactions
                count is the number of elements in the interval of length t starting at best_t
    :best time complexity: O(1)
    :worst time complexity: O(kN), k is the greatest number of digits in any element of transactions
                                   N is the number of elements in transactions
    :aux space complexity: O(N+M), M is the number of unique non-negative integers of the base
                                   in counting_sort(lst, exp)
    """
    # if the transaction records are empty
    if len(transactions) == 0:
        return (0, 0)
    else:
        #sort transactions list
        transactions = radix_sort(transactions)
        i, j, end, count, longest_count, best_t = 0, 0, 0, 0, 0, 0
        # loop to the end of the list
        # end if the number of unchecked elements is less than count
        while len(transactions)-i > longest_count and j < len(transactions):
            # if element is within interval
            if transactions[j] <= transactions[i]+t:
                # increase count and check subsequent element
                count += 1
                j += 1
                if count > longest_count:
                    longest_count = count
                    end = j-1
            else:
                i += 1
                # if the current starting time is the same as the previous, go to the next
                if i < len(transactions) and transactions[i] == transactions[i-1]:
                    i += 1
                j = i
                count = 0
        # calculate the minimal starting time
        if transactions[end]-t >= 0:
            best_t = transactions[end]-t
        else:
            best_t = 0
        return (best_t, longest_count)


########## Question 2 ##########
#%%
def sort_word(word):
    """
    Sorts a string in alphabetical order
    :param word: string consisting of lowercase a-z
    :return: sorted word in alphabetical order
    :best time complexity: O(1)
    :worst time complexity: O(N+M), N is the number of characters in word
                                    M is the number of characters of the base, which is lowercase a-z
    :aux space complexity: O(N+M)
    """
    # empty string or string with one character is already sorted
    if len(word) <= 1:
        return word
    else:
        base = 26
        # initialise count array
        count_arr = [0] * base
        # update count array
        for char in word:
            count_arr[ord(char)-97] += 1
        # sort the word
        sorted_word = ""
        for i in range(len(count_arr)):
            for _ in range(count_arr[i]):
                sorted_word += chr(i+97)
        return sorted_word

#%%
def counting_sort_alpha(lst, pos):
    """
    Sorts the tuple in the list according to the first element of the tuple, string consisting of
    lowercase a-z in a stable manner based on the k-th alphabet from the right determined by pos
    :param lst: list of two tuple element, (string, int)
    :param pos: column of alphabet from the right of the string to be compared
    :return: sorted list based on the k-th alphabet from the right of the string in non-decreasing order
    :best time complexity: O(N+M), N is the number of elements in lst
                                   M is the number of unique characters of the base
    :worst time complexity: O(N+M)
    :aux space complexity: O(N+M)
    """
    # two extra base, for empty string and string that is shorter than k-th column
    base = 28
    # initialise count array
    count_arr = [None] * base
    for i in range(len(count_arr)):
        count_arr[i] = []
    # update count array
    for j in range(len(lst)):
        word = lst[j][0]
        if len(word) == 0:
            col = 0
        elif len(word) <= pos:
            col = 1
        else:
            col = ord(word[-(pos+1)])-97+2
        count_arr[col].append(lst[j])
    # update lst by putting each element at the correct index
    index = 0
    for a in range(len(count_arr)):
        for b in range(len(count_arr[a])):
            lst[index] = count_arr[a][b]
            index += 1
    return lst

#%%
def radix_sort_alpha(lst):
    """
    Takes a list of strings, convert into two element tuple (string, i), where i is the
    original index of the string in lst
    Sorts the new list based on the strings in the tuple, column by column from the rightmost alphabet
    to the leftmost alphabet in a non-decreasing manner using ASCII value
    :param lst: list of strings
    :return: sorted list of tuples according to the string, the first elemnt in the tuple
    :best time complexity: O(1)
    :worst time complexity: O(kN), k is the length of the longest string in lst
                                   N is the number of elements in lst
    :aux space complexity: O(N+M), M is the number of unique characters of the base
                                   in counting_sort_alpha(lst, pos)
    """
    if len(lst) <= 0:
        return lst
    # find longest string
    max_char = len(max(lst, key = len))
    # tranform items in lst to be a tuple with original index
    for i in range(len(lst)):
        lst[i] = (lst[i], i)
    # sort list
    for j in range(max_char):
        counting_sort_alpha(lst, j)
    return lst

#%%
def words_with_anagrams(list1, list2):
    """
    From two lists of words, ind all words in the first list which have an anagram in the second list from
    :param list1: list of unique strings, all characters lowercase a-z
    :param list2: list of unique strings, all characters lowercase a-z
    :return: list of words in list1 which have an anagram in list2
    :best time complexity: O(L1M1 + L2M2), L1 is the number of elements in list1
                                           L2 is the numebr of elements in list2
                                           M1 is the number of characters in the longest string in list1
                                           M2 is the number of characters in the longest string in list2
    :worst time complexity: O(L1M1 + L2M2)
    :aux space complexity: O(L1+L2+M1+M2+k), k is the number of elements in output which is the number of
                                             strings in list1which have at least one anagram in list2
    """
    # sort each word in list1 and copy to new string
    # O(L1M1)
    list1_sorted = []
    for i in range(len(list1)):
        list1_sorted.append(sort_word(list1[i]))
    # sort each word in list2
    # O(L2M2)
    for j in range(len(list2)):
        list2[j] = sort_word(list2[j])
    # radix sort list1_sorted and list2
    list1_sorted = radix_sort_alpha(list1_sorted)
    list2 = radix_sort_alpha(list2)
    # compare sorted words from both sorted lists
    i, j = 0, 0
    output = []
    while i < len(list1) and j < len(list2):
        # access the word from the tuple
        str1 = list1_sorted[i][0]
        str2 = list2[j][0]
        # if length of words are the same, compare words
        if len(str1) == len(str2):
            # if both strings are equal, find original word in list1 with the index in tuple
            # append to output
            if str1 == str2:
                output.append(list1[list1_sorted[i][1]])
                i += 1
            # compare each word in both lists at most 2 times
            elif str1 < str2:
                i += 1
            else:
                j += 1
        # if length of word from list2 is longer, go to next word in list1
        elif len(str1) < len(str2):
            i += 1
        # if length of word from list1 is longer, go to the next word is list2
        else:
            j += 1
    return output

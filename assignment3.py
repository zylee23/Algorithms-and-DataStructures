"""
Name: Lee Zi Yan
Student ID: 31264689
"""

#%%
class PrefixNode:
    def __init__(self):
        """
        Initialise an instance of a node in a prefix trie
        :best time complexity: O(1)
        :worst time complexity: O(1)
        :aux space complexity: O(1)
        """
        # highest frequency of the string with prefix from root to node
        self.freq = 0
        # string with the highest frequency with prefix from root to node
        self.data = None
        # possible children of a node, terminal at index 0
        self.link = [None] * 5
        # child with lowest lexi order
        self.least = None


class SequenceDatabase:
    def __init__(self):
        """
        Initialise an instance of a SequenceDatabse which is a prefix trie
        :best time complexity: O(1)
        :worst time complexity: O(1)
        :aux space complexity: O(1)
        """
        # creates the root of the trie
        self.root = PrefixNode()

    def addSequence(self, s):
        """
        Store s into the instance of SequenceDatabase
        :param s: nonempty string of uppercase letters in uppercase [A-D]
        :best time complexity: O(len(s))
        :worst time complexity: O(len(s))
        :aux space complexity: O(len(s)) if the nodes do no exist
        """
        self.aux_addSequence(self.root, s, 0)

    def aux_addSequence(self, curr, s, i):
        """
        Recursive method to store s into the instance of SequenceDatabase
        Updates the data in the node during return
        :param curr: current node of the trie
        :param s: nonempty string of uppercase letters in uppercase [A-D]
        :param i: current index of s
        :return curr.freq: frequency of s in the database
        :best time complexity: O(len(s))
        :worst time complexity: O(len(s))
        :aux space complexity: O(len(s)) if the nodes do no exist
        """
        # if at leaf, increase freq
        if i > len(s):
            curr.freq += 1
            curr.least = 0
            curr.data = s
        else:
            index = ord(s[i]) - 64 if i < len(s) else 0
            # create or go to child node
            nextNode = self.returnNext(curr, index)
            # insert the next character of string to child node
            newFreq = self.aux_addSequence(nextNode, s, i+1)
            # newFreq is the frequency of s in the database
            # if freq of added string is greater than the freq stored at the node
            if newFreq > curr.freq:
                curr.freq = newFreq
                curr.least = index
                curr.data = s
            # if freq is the same, choose string with lower lexi order
            # compare string of child node with string stored at the node
            elif newFreq == curr.freq:
                if index <= curr.least:
                    curr.least = index
                    curr.data = nextNode.data
        return curr.freq

    def returnNext(self, curr, i):
        """
        Creates a specified child node based on index if it does not exist
        :param curr: current node of the trie
        :param i: index of child node in self.link
        :return curr.link[i]: child node
        :best time complexity: O(1)
        :worst time complexity: O(1)
        :aux space complexity: O(1)
        """
        if curr.link[i] == None:
            curr.link[i] = PrefixNode()
        return curr.link[i]

    def query(self, q):
        """
        Return the string from database with highest frequency and lowest lexi order with q as prefix
        :param q: possibly empty string of uppercase letters in uppercase [A-D]
        :return curr.data: data stored at the node after traversing through the trie
        :return None: if no such string exists
        :best time complexity: O(1) if q does not exist
        :worst time complexity: O(len(q))
        :aux space complexity: O(1)
        """
        # start at root of trie
        curr = self.root
        # traverse until final char of q
        for char in q:
            index = ord(char) - 64
            if curr.link[index] != None:
                curr = curr.link[index]
            else:
                return None
        return curr.data

# %%
class SuffixNode:
    def __init__(self):
        """
        Initialise an instance of a node in a suffix trie
        :best time complexity: O(1)
        :worst time complexity: O(1)
        :aux space complexity: O(1)
        """
        # the indices of characters in the string
        self.occ = []
        # possible children of a node, terminal at index 0
        self.link = [None] * 5

class OrfFinder:
    def __init__(self, genome):
        """
        Initialise an instance of a OrfFinder by creating a suffix trie of input string
        :param genome: non-empty string consisting only of uppercase [A-D]
        :best time complexity: O(N^2) where N is the length of genome
        :worst time complexity: O(N^2)
        :aux space complexity: O(N^2)
        """
        self.genome = genome
        # creates the node of the trie
        self.root = SuffixNode()
        self.createSuffixTrie(genome)

    def createSuffixTrie(self, s):
        """
        Create a suffix trie of the input string
        :param s: non-empty string consisting only of uppercase [A-D]
        :best time complexity: O(N^2) where N is the length of genome
        :worst time complexity: O(N^2)
        :aux space complexity: O(N^2)
        """
        # an empty string is also a suffix
        self.root.link[0] = SuffixNode()

        # create suffix trie
        for i in range(len(s)):
            # start from root
            curr = self.root
            # for every suffix
            for j in range(i, len(s)):
                index = ord(s[j]) - 64
                # create child node if it does not exist
                if curr.link[index] == None:
                    curr.link[index] = SuffixNode()
                # go to child ndoe and store current index of string
                curr = curr.link[index]
                curr.occ.append(j)
            # add terminal node
            curr.link[0] = SuffixNode()

    def find(self, start, end):
        """
        Find all the substrings of genome which have start as a prefix and end as a suffix in no particular order
        Start and end must not overlap in the substring
        :param start: non-empty string consisting of only uppercase [A-D]
        :param end: non-empty string consisting of only uppercase [A-D]
        :return ret: a list of strings which are the substrings of genome
        :best time complexity: O(1) if start and end does not exist
        :worst time complexity: O(len(start) + len(end) + U) where U is the number of characters in the output list
        :aux space complexity:
        """
        # check if start and end exist in suffix trie
        first = self.checkExists(start)
        last = self.checkExists(end)

        # if start or end does not exist
        if first == None or last == None:
            return []
        # if start occurs before end
        elif first.occ[0] < last.occ[0] or first.occ[0] < last.occ[-1]:
            ret = self.substrings(start, end, first, last)
            return ret
        else:
            return []

    def substrings(self, start, end, first, last):
        """
        List all substrings with start as prefix and end as suffix if stast and end exist in trie
        :param start: non-empty string consisting of only uppercase [A-D]
        :param end: non-empty string consisting of only uppercase [A-D]
        :param first: node after traversing start
        :param last: node after traversing end
        :best time complexity: O(1) if start and end overlap
        :worst time complexity: O(U) where U is the number of characters in the output list
        :aux space complexity: O(U)
        """
        ret = []
        # first.occ contains index of start in stored genome
        for i in first.occ:
            # last.occ contains index of end in stored genome
            for j in last.occ:
                # if current index of prefix occurs after start
                # if start and end does not overlap
                if i+1 >= len(start) and j-i >= len(end):
                    # slice the substring from stored genome and add to output list
                    ret.append(self.genome[i-len(start)+1:j+1])
        return ret

    def checkExists(self, s):
        """
        Checks if a string exists in the suffix trie
        :param s: non-empty string consisting of only uppercase [A-D]
        :return curr: last node after traversing through trie
        :return None: if no such string exists
        :best time complexity: O(1) if string does not exist
        :worst time complexity: O(len(s))
        :aux space complexity: O(1)
        """
        curr = self.root
        for char in s:
            index = ord(char) - 64
            if curr.link[index] != None:
                curr = curr.link[index]
            else:
                return None
        return curr
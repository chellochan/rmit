from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency

# ------------------------------------------------------------------------
# This class is required TO BE IMPLEMENTED
# Trie-based dictionary implementation
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------


# Class representing a node in the Trie
class TrieNode:

    def __init__(self, letter=None, frequency=None, is_last=False):
        self.letter = letter            # letter stored at this node
        self.frequency = frequency      # frequency of the word if this letter is the end of a word
        self.is_last = is_last          # True if this letter is the end of a word
        self.children: dict[str, TrieNode] = {}     # a hashtable containing children nodes, key = letter, value = child node
    #
    # def __str__(self):
    #     return "letter: {}, frequency: {}, is_last: {}, length of child: {}"\
    #         .format(self.letter, self.frequency, str(self.is_last), len(self.children))


class TrieDictionary(BaseDictionary):

    def __init__(self):
        self.__root = TrieNode()

    @property
    def root(self):
        return self.__root

    def build_dictionary(self, words_frequencies: [WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        for word_freq in words_frequencies:
            self.add_word_frequency(word_freq)

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        cur_node = self.root
        word_idx = 0
        while cur_node:
            next_node = cur_node.children.get(word[word_idx])
            isLast = len(word) == (word_idx + 1)

            if next_node:
                if isLast:
                    if next_node.is_last:
                        return next_node.frequency
                    else:
                        return 0
                else:
                    cur_node = next_node
                    word_idx += 1
            else:
                return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        is_exist = self.search(word_frequency.word) != 0
        if not is_exist:
            cur_node = self.root
            word_idx = 0
            while cur_node:
                next_node = cur_node.children.get(word_frequency.word[word_idx])

                frequency = None
                isLast = False
                if len(word_frequency.word) == (word_idx + 1):
                    frequency = word_frequency.frequency
                    isLast = True

                if not next_node:
                    # i.e. new char
                    next_node = TrieNode(word_frequency.word[word_idx], frequency, isLast)
                    cur_node.children[next_node.letter] = next_node

                if isLast:
                    next_node.is_last = True
                    next_node.frequency = word_frequency.frequency
                    cur_node = None
                else:
                    cur_node = next_node
                    word_idx += 1
            return True
        return False

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        is_exist = self.search(word) != 0
        if is_exist:
            cur_node = self.root
            word_idx = 0
            while cur_node:
                next_node = cur_node.children.get(word[word_idx])
                is_last = len(word) == (word_idx + 1)

                if is_last:
                    if len(next_node.children) > 0:
                        next_node.is_last = False
                        next_node.frequency = None
                    else:
                        cur_node.children[word[word_idx]] = None
                    return True
                else:
                    cur_node = next_node
                    word_idx += 1
        return False

    def autocomplete(self, word: str) -> [WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        return_arr = []
        cur_node = self.root
        word_idx = 0
        last_node = None
        str_prefix = ""
        while cur_node:
            next_node = cur_node.children.get(word[word_idx])
            if next_node and next_node.letter:
                str_prefix += next_node.letter

            is_end_suggest_word = len(word) == (word_idx + 1)

            if is_end_suggest_word:
                last_node = next_node
                if last_node:
                    if last_node.is_last:
                        return_arr.append(WordFrequency(word, next_node.frequency))
                    TrieDictionary.add_word_frequency_with_parent_node(return_arr, last_node, str_prefix)
                cur_node = None
            else:
                if next_node:
                    cur_node = next_node
                    word_idx += 1
                else:
                    cur_node = None
        return_arr.sort(key=lambda x: x.frequency, reverse=True)

        return return_arr[:3]

    @staticmethod
    def add_word_frequency_with_parent_node(arr: [WordFrequency], parent_node: TrieNode, parent_word: str):
        word = parent_word
        for child_node in parent_node.children.values():
            # print("add_word_frequency_with_parent_node2: {}".format(arr))
            if child_node:
                if child_node.is_last:
                    arr.append(WordFrequency((parent_word + child_node.letter), child_node.frequency))

                if len(child_node.children) > 0:
                    w = word + child_node.letter
                    TrieDictionary.add_word_frequency_with_parent_node(arr, child_node, w)
        # print("add_word_frequency_with_parent_node: {}".format(arr))

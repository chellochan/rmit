from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency

class ListNode:
    '''
    Define a node in the linked list
    '''

    def __init__(self, word_frequency: WordFrequency):
        self.word_frequency = word_frequency
        self.next = None


# ------------------------------------------------------------------------
# This class  is required TO BE IMPLEMENTED
# Linked-List-based dictionary implementation
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------

class LinkedListDictionary(BaseDictionary):

    def __init__(self):
        self.__m_head = None
        self.__m_length = 0

    @property
    def m_head(self):
        return self.__m_head

    @m_head.setter
    def m_head(self, m_head):
        self.__m_head = m_head

    @property
    def m_length(self):
        return self.__m_length

    @m_length.setter
    def m_length(self, m_length):
        self.__m_length = m_length

    def build_dictionary(self, words_frequencies: [WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        prev_node = None

        for word_frequency in words_frequencies:
            cur_node = ListNode(word_frequency)
            if not self.m_head:
                self.m_head = cur_node
            if prev_node:
                prev_node.next = cur_node
            self.m_length += 1
            prev_node = cur_node

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        cur_node = self.m_head
        for i in range(self.m_length):
            if cur_node.word_frequency.word == word:
                if cur_node.word_frequency.frequency > 0:
                    return cur_node.word_frequency.frequency
                else:
                    return 0
            cur_node = cur_node.next
        return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        cur_node = self.m_head
        last_node = None

        while cur_node:
            if cur_node.word_frequency.word == word_frequency.word:
                return False

            if cur_node.next:
                cur_node = cur_node.next
            else:
                last_node = cur_node
                cur_node = None

        add_node = ListNode(word_frequency)
        if last_node:
            last_node.next = add_node
        else:
            self.m_head = add_node
        self.m_length += 1

        return True

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        cur_node = self.m_head
        prev_node = None

        while cur_node:
            if cur_node.word_frequency.word == word:
                if prev_node:
                    prev_node.next = cur_node.next
                else:
                    self.m_head = cur_node.next

                self.m_length -= 1
                return True

            if cur_node.next:
                prev_node = cur_node
                cur_node = cur_node.next
            else:
                cur_node = None

        return False

    def autocomplete(self, word: str) -> [WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        return_arr = []
        cur_node = self.m_head

        while cur_node:
            word_len = len(word)
            if cur_node.word_frequency.word[:word_len] == word:
                return_arr.append(cur_node.word_frequency)

            if cur_node.next:
                cur_node = cur_node.next
            else:
                cur_node = None

        return_arr.sort(key=lambda x: x.frequency, reverse=True)

        return return_arr[:3]

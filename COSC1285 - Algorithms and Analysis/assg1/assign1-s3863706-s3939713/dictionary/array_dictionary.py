from dictionary.word_frequency import WordFrequency
from dictionary.base_dictionary import BaseDictionary

# ------------------------------------------------------------------------
# This class is required TO BE IMPLEMENTED
# Array-based dictionary implementation
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------

class ArrayDictionary(BaseDictionary):

    def __init__(self):
        self.__arr = []
        pass

    @property
    def arr(self):
        return self.__arr

    @arr.setter
    def arr(self, arr):
        self.__arr = arr

    def build_dictionary(self, words_frequencies: [WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        for word_frequency in words_frequencies:
            self.arr.append(word_frequency)
            pass
        self.arr.sort(key=lambda x: x.word)

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        for word_freq in self.arr:
            if word_freq.word == word:
                return word_freq.frequency
        return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        freq = self.search(word_frequency.word)
        if freq == 0:
            i = 0
            for word_freq in self.arr:
                if word_frequency.word > word_freq.word:
                    i += 1
                    break
            self.arr.insert(i, word_frequency)

            return True
        else:
            return False

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        # find the position of 'word' in the list, if exists, will be at idx-1
        freq = self.search(word)
        if freq > 0:
            i = 0
            for word_freq in self.arr:
                if word == word_freq.word:
                    break
                i += 1
            self.arr.pop(i)

            return True
        else:
            return False

    def autocomplete(self, prefix_word: str) -> [WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'prefix_word' as a prefix
        @param prefix_word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'prefix_word'
        """
        return_arr = []
        for word_freq in self.arr:
            prefix_word_len = len(prefix_word)
            if word_freq.word[:prefix_word_len] == prefix_word:
                return_arr.append(word_freq)

        return_arr.sort(key=lambda x: x.frequency, reverse=True)

        return return_arr[:3]

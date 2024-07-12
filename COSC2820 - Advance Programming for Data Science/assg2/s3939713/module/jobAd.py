from itertools import chain

from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize

import re


class JobAd:
    def __init__(self, file_path, data, job_category):
        self.__file_path = file_path  # relative file path from the file
        self.__raw_data = data  # raw data is for read only, should not be amended
        self.__job_category = job_category  # i.e. folder name
        self.__data = {}  # data dictionary for storing contents by title, webindex, company & desc
        self.__desc_tokens = []  # list for storing description tokens for pre-processing
        self.__title_tokens = []  # list for storing description tokens for pre-processing
        self.__desc_token_count_dict = {}  # for Task 2
        self.__title_token_count_dict = {}  # for Task 3
        self.__all_token_count_dict = {}  # for Task 3
        # initialize data from raw data
        self.load_raw_data()
        pass

    @property
    def file_path(self):
        return self.__file_path

    @property
    def raw_data(self):
        return self.__raw_data

    @property
    def job_category(self):
        return self.__job_category

    @property
    def data(self):
        return self.__data

    @property
    def desc_tokens(self):
        return self.__desc_tokens

    @desc_tokens.setter
    def desc_tokens(self, desc_tokens):
        self.__desc_tokens = desc_tokens

    @property
    def title_tokens(self):
        return self.__title_tokens

    @title_tokens.setter
    def title_tokens(self, title_tokens):
        self.__title_tokens = title_tokens

    @property
    def desc_token_count_dict(self):
        return self.__desc_token_count_dict

    @property
    def title_token_count_dict(self):
        return self.__title_token_count_dict

    @property
    def all_token_count_dict(self):
        return self.__all_token_count_dict

    @property
    def all_tokens(self):
        return self.__title_tokens + self.__desc_tokens

    def get_value_from_data(self, key):
        '''return value of data dictionary with specified key
        '''
        if key in self.data:
            return self.data[key]
        return None

    def get_title(self):
        '''return title from data dictionary
        '''
        return self.get_value_from_data('Title')

    def get_web_index(self):
        '''return web index from data dictionary
        '''
        return self.get_value_from_data('Webindex')

    def get_company(self):
        '''return company from data dictionary
        (could be None if there is no company in raw data)
        '''
        return self.get_value_from_data('Company')

    def get_desc(self):
        '''return description from data dictionary
        '''
        return self.get_value_from_data('Description')

    def add_data(self, key, value):
        ''' add value to data dictionary
        '''
        self.data[key] = value

    def raw_data_lines(self):
        '''return an array of raw data split by lines(i.e. "\n")
        '''
        return self.__raw_data.split("\n")

    def load_raw_data(self):
        '''convert raw data into data dictionary by splitting lines
        and some regular expression
        '''
        type_pattern = r"^([a-zA-Z0-9]+)\:\s?(.*)"
        pattern = re.compile(type_pattern)
        for line in self.raw_data_lines():
            match = pattern.match(line)
            if match:
                self.add_data(match.group(1), match.group(2))
            else:
                print("Warning! Pattern not match. file: {}, line: {}" \
                      .format(self.file_path, line))

    def tokenizeDesc(self, pattern = r"[a-zA-Z]+(?:[-'][a-zA-Z]+)?"):
        '''tokenize description from self.get_desc()
        it fulfills Task 1 pt. 1, 2 & 3
        '''
        # Task 1 pt. 1 & 3
        nl_desc = self.get_desc().lower()
        sentences = sent_tokenize(nl_desc)

        # Task 1 pt. 2
        tokenizer = RegexpTokenizer(pattern)

        token_lists = [tokenizer.tokenize(sen) for sen in sentences]
        self.desc_tokens = list(chain.from_iterable(token_lists))

    def tokenizeTitle(self, pattern = r"[a-zA-Z]+(?:[-'][a-zA-Z]+)?"):
        '''tokenize title from self.get_title()
        Task3
        '''
        nl_title = self.get_title().lower()
        sentences = sent_tokenize(nl_title)
        tokenizer = RegexpTokenizer(pattern)

        token_lists = [tokenizer.tokenize(sen) for sen in sentences]
        self.title_tokens = list(chain.from_iterable(token_lists))

    def remove_words(self, length=2):
        '''remove words with specific length (default length is 2)
        assign back to self.desc_tokens
        Task 1 pt. 4
        '''
        self.desc_tokens = [w for w in self.desc_tokens if len(w) >= length]

    def remove_by_list(self, remove_list):
        '''remove self.desc_tokens which is in remove_list
        assign back to self.desc_tokens
        Task 1 pt. 4, 5 & 6
        '''
        self.desc_tokens = [desc_token for desc_token in self.desc_tokens \
                            if desc_token not in remove_list]

    def count_desc_tokens(self, token_list):
        '''count token saving in dictionary
        Task 2
        '''
        for desc_token in self.desc_tokens:
            if desc_token in token_list:
                if desc_token in self.desc_token_count_dict:
                    self.desc_token_count_dict[desc_token] += 1
                else:
                    self.desc_token_count_dict[desc_token] = 1

    def count_title_tokens(self, token_list):
        '''count token saving in dictionary
        Task 2
        '''
        for token in self.title_tokens:
            if token in token_list:
                if token in self.title_token_count_dict:
                    self.title_token_count_dict[token] += 1
                else:
                    self.title_token_count_dict[token] = 1

    def count_all_tokens(self, token_list):
        '''count token saving in dictionary
        Task 2
        '''
        for token in self.all_tokens:
            if token in token_list:
                if token in self.all_token_count_dict:
                    self.all_token_count_dict[token] += 1
                else:
                    self.all_token_count_dict[token] = 1

    def __str__(self):
        return "File_path: {file_path},\nJob category: {cat},\nTitle: {title},\n" \
               "Web index: {web_idx},\nCompany: {company},\nDesc: {desc},\nRaw: {raw},\n" \
               "Data: {data},\nDesc Tokens: {desc_token},\nDesc Token Dict: {desc_token_dict}".format(
            file_path=self.__file_path,
            cat=self.__job_category,
            raw=None,
            data=None,
            title=self.get_title(),
            web_idx=self.get_web_index(),
            company=self.get_company(),
            desc=self.get_desc(),
            desc_token=self.desc_tokens,
            desc_token_dict=self.desc_token_count_dict
        )

import os
import re
from itertools import chain

import numpy as np
import pandas as pd
from nltk.probability import *
from scipy.sparse import csr_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold

from module.jobAd import JobAd


def read_job_ad(dir_path="./data"):
    '''
    to read all contents from specified path
    :param dir_path:
    :return:
    '''
    job_category = []
    job_ad_list = []

    for folder_name in sorted(os.listdir(dir_path)):
        # check with folder name is a directory
        if os.path.isdir(os.path.join(dir_path, folder_name)):
            # use folder name as job category
            job_category.append(folder_name)
            # list all files in job category folder
            for filename in sorted(os.listdir(os.path.join(dir_path, folder_name))):
                file_full_path = os.path.join(dir_path, folder_name, filename)
                # check file is a file
                if os.path.isfile(os.path.join(file_full_path)):
                    # open the txt file with utf-8 (for 's)
                    with open(file_full_path, "r", encoding='utf-8') as f:  # open the txt file
                        # create a JobAd object and initialize the object
                        job_ad_list.append(JobAd(file_full_path, f.read(), folder_name))
                        f.close()
    return job_ad_list, job_category


def read_stopwords(path="stopwords_en.txt", permission="r", encoding="utf-8"):
    '''function to read all stop words in stopwords_en.txt
    splitting stopwords by line indicator(\n)
    storing stopwords in a list and return
    Task 1 pt. 5
    '''
    stopword_lists = []
    with open(path, permission, encoding=encoding) as f: # open the txt file
        full_stopword = f.read()
        stopword_lists = full_stopword.split("\n")
        f.close()
    return stopword_lists


def read_vocab(path="vocab.txt"):
    ''' read vocab in vocab.txt
    with pattern r"^(.*):(.*)$"
    return a dictionary
    '''
    vocab_dict = {}
    pattern = r"^(.*):(.*)$"
    file_vocab = os.path.join(path)
    with open(file_vocab, "r", encoding='utf-8') as f:
        vocabs = f.readlines()
        f.close()
    for vocab in vocabs:
        p = re.compile(pattern)
        match = p.match(vocab)
        if match:
            vocab_dict[match.group(1)] = int(match.group(2))
        # else:
            # print("Warning! Pattern not match. file: {}, line: {}" \
            #       .format(self.file_path, line))
    return vocab_dict


def save_count_vector(job_ad_list, vocab_dict, path="count_vectors.txt", permission="w+", encoding="utf-8"):
    '''
    save count_vectors.txt for Task 2
    :param job_ad_list:
    :param vocab_dict:
    :param path:
    :param permission:
    :param encoding:
    :return:
    '''
    with open(path, permission, encoding=encoding) as f:
        # sort job_ad_list by web index
        # int(job_ad.get_web_index()) because for sorting int vs sorting str
        job_ad_list.sort(key=lambda jobAd: int(jobAd.get_web_index()))
        for job_ad in job_ad_list:
            tmp_dict = {}  # tmp_dict for saving token count for sorted printing
            for token in job_ad.desc_tokens:
                tmp_dict[vocab_dict[token]] = job_ad.desc_token_count_dict[token]
            word_freq_txt = ""
            # sort tmp_dict by key (word_idx type: int)
            for word_idx in sorted(tmp_dict):
                word_freq_txt += "{}:{},".format(word_idx, tmp_dict[word_idx])
            f.write("#{},{}\n".format(job_ad.get_web_index(), word_freq_txt[:len(word_freq_txt) - 1]))
        f.close()


def generate_corpus_file(job_ad_list, path="job_ad_all.txt", permission="w+", encoding="utf-8"):
    with open(path, permission, encoding=encoding) as f:
        # sort job_ad_list by web index
        # int(job_ad.get_web_index()) because for sorting int vs sorting str
        job_ad_list.sort(key=lambda job_ad: int(job_ad.get_web_index()))
        for job_ad in job_ad_list:
            f.write(" ".join(job_ad.desc_tokens))
            f.write('\n')
        f.close()


def summarise_words(job_ad_list, prev_words_list=[]):
    '''
    for printing the summary of job advertisement list before and after change
    :param job_ad_list:
    :param prev_words_list:
    :return:
    '''
    all_words = list(chain.from_iterable([job_ad.desc_tokens for job_ad in job_ad_list]))
    print("Words: {}\nVocabs: {}".format(len(all_words), len(set(all_words))))
    if prev_words_list:
        print("Removed Words: {}\nRemoved Vocabs: {}".format(
            len(prev_words_list) - len(all_words),
            len(set(prev_words_list)) - len(set(all_words))))
    return all_words

def preprocess():
    '''
    preprocess procedures in Part 1 (for Part 2&3)
    :return:
    '''
    result = read_job_ad()
    job_ad_list = result[0]
    job_category = result[1]

    stopword_lists = read_stopwords()
    for job_ad in job_ad_list:
        job_ad.tokenizeDesc()
    for job_ad in job_ad_list:
        job_ad.remove_words()
    for job_ad in job_ad_list:
        job_ad.remove_by_list(stopword_lists)

    words = list(chain.from_iterable([job_ad.desc_tokens for job_ad in job_ad_list]))
    term_fd = FreqDist(words)

    # Filtering a word list which appear once only
    appear_1_list = [df[0] for df in list(term_fd.items()) if df[1] == 1]

    for job_ad in job_ad_list:
        job_ad.remove_by_list(appear_1_list)

    words_2 = list(chain.from_iterable([set(job_ad.desc_tokens) for job_ad in job_ad_list]))
    term_fd_2 = FreqDist(words_2)
    most_50_common_keys = [fd[0] for fd in term_fd_2.most_common(50)]
    for job_ad in job_ad_list:
        job_ad.remove_by_list(most_50_common_keys)
        job_ad.tokenizeTitle()
    return result


def generate_list_for_modelling(job_ad_list, vocab_list, vector_size, tfidf_features, model_ft, token_type, return_as_matrix=False):
    '''
    Use job advertisements to generate 3 models, count-vector model, unweighted word embedding model with FastText and
    Tf-idf weighted word embedding model with FastText.
    Return for plotting TSN or run ML model.
    :param job_ad_list: list
    :param vocab_list: list
    :param vector_size: int
    :param tfidf_features:
    :param model_ft: Fasttext
    :param token_type: str
    :param return_as_matrix: bool
    :return: (np.array, np.array, np.array) / (martrix, martrix, martrix)
    '''
    count_x=[]
    unweighted_x=[]
    weighted_x=[]
    errors=0

    for job_ad_idx, job_ad in enumerate(job_ad_list):
        tokens=[]
        token_count_dict={}
        if token_type == "desc":
            tokens = job_ad.desc_tokens
            token_count_dict = job_ad.desc_token_count_dict
        elif token_type == "title":
            tokens = job_ad.title_tokens
            token_count_dict = job_ad.title_token_count_dict
        elif token_type == "all":
            tokens = job_ad.all_tokens
            token_count_dict = job_ad.all_token_count_dict
        num_words=len(tokens)
        sum_words=0
        weight_sum=0
        count_list=np.zeros(len(vocab_list))

        sent_vec = np.zeros(vector_size)
        for word in tokens:
            # if word in job_ad.token_count_dict:
            count_list[vocab_list.index(word)] = (token_count_dict[word] if word in token_count_dict else 0)
            sum_words+=model_ft.wv[word]
            try:
                vec = model_ft.wv[word]
                # obtain the tf_idfidf of a word in a sentence/review
                # tfidf_feat = tfidf_features.get_feature_names()
                tfidf = tfidf_features[job_ad_idx, vocab_list.index(word)]
                sent_vec += (vec * tfidf)
                weight_sum += tfidf
            except:
                errors =+1
                pass
        sent_vec /= weight_sum
        count_x.append(np.array(count_list))
        unweighted_x.append(sum_words/num_words)
        weighted_x.append(sent_vec)
    print("errors noted: "+str(errors))
    if return_as_matrix:
        return csr_matrix(count_x), csr_matrix(unweighted_x), csr_matrix(weighted_x)
    else:
        return count_x, unweighted_x, weighted_x


def evaluate(X_train,X_test,y_train, y_test,seed):
    '''
    evaluate the result with Logistic Regression ML model
    :param X_train:
    :param X_test:
    :param y_train:
    :param y_test:
    :param seed:
    :return:
    '''
    model = LogisticRegression(random_state=seed)
    model.fit(X_train, y_train)
    return model.score(X_test, y_test)


def generate_cv_df(count_x_matrix, unweighted_x_matrix, weighted_x_matrix, category_series, seed=0):
    '''
    run and generate result by selected ML algorithm with 3 different language models
    :param count_x_matrix:
    :param unweighted_x_matrix:
    :param weighted_x_matrix:
    :param category_series:
    :param seed:
    :return:
    '''
    if count_x_matrix is None and unweighted_x_matrix is None and weighted_x_matrix is None:
        raise RuntimeError("All matrices are None")
    num_folds = 5
    kf = KFold(n_splits=num_folds, random_state=seed, shuffle=True)  # initialise a 5 fold validation

    category_list = category_series.tolist()
    num_models = 3
    columns = []
    if count_x_matrix is not None:
        columns.append("count")
    if unweighted_x_matrix is not None:
        columns.append("unweighted")
    if weighted_x_matrix is not None:
        columns.append("tfidf-weighted")
    cv_df = pd.DataFrame(columns = columns,index=range(num_folds)) # creates a dataframe to store the accuracy scores in all the folds

    fold = 0
    for train_index, test_index in kf.split(list(range(0,len(category_series)))):
        y_train = [category_list[i] for i in train_index]
        y_test = [category_list[i] for i in test_index]

        if count_x_matrix is not None:
            cv_df.loc[fold,"count"] = evaluate(count_x_matrix[train_index],count_x_matrix[test_index],y_train,y_test,seed)
        if unweighted_x_matrix is not None:
            cv_df.loc[fold,"tfidf"] = evaluate(unweighted_x_matrix[train_index],unweighted_x_matrix[test_index],y_train,y_test,seed)
        if weighted_x_matrix is not None:
            cv_df.loc[fold,"weighted-tfidf"] = evaluate(weighted_x_matrix[train_index],weighted_x_matrix[test_index],y_train,y_test,seed)

        fold +=1
    return cv_df

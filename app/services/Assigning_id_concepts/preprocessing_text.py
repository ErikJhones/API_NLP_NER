import nltk    
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk import tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.tree import Tree
from nltk.chunk import conlltags2tree


import re
import os
import html2text
import numpy as np
from mtranslate import translate
import pandas as pd

def removing_html_noise(text: str):
    """ 
    function that removes html tags from an input string.

    Parameters
    ----------
    text str: clinical note.
    
    Return
    ------
    word str: clinical note without html tags.
    """

    caracte = ['\n', '\r', '\p', '\t', '\d']
    word = ''
    word = html2text.html2text(text)
    
    for carac in caracte:
        word = word.replace(carac, ' ')

    return word

def group_word_by_ner(text: list, ner: list):
    """ 
    function that groups tokens based on NERs 
    (EX: [(5, B-DT), (months, I-DT)] == [(5 months, DT)])

    Parameters
    ----------
    text list: clinical note's tokens.
    
    ner list: clinical note tokens' ner.

    Return
    ------
    original_text list: list with the grouped tokens and their ners.
    """

    pos_tags = [pos for token, pos in pos_tag(text[0])]
    conlltags = [(token, pos, tg) for token, pos, tg in zip(text[0], pos_tags, ner[0])]
    ne_tree = conlltags2tree(conlltags)
    original_text = []
    texto = []
    idx = 0
    for subtree in ne_tree:
        if type(subtree) == Tree:
            original_label = subtree.label()
            original_string = " ".join([token for token, pos in subtree.leaves()])
            texto.append(original_string)
            original_text.append([original_string, original_label, str(idx)])
        else:
            original_text.append([subtree[0], 'O', str(idx)])
        idx+=1
    return original_text

def filtring_dates(group_text: list):
    jj = []
    idx=0
    for i in group_text:
        if i[1] == 'DT':
            for j in i[0].split():
                jj.append([j, 'DT', str(idx)])
                idx+=1
        else:
            jj.append([i[0], i[1], str(idx)])
            
            idx+=1
    return jj

def translating(text: list):
    """ 
    function that translates tokens to English.

    Parameters
    ----------
    text list: clinical note's tokens.

    Return
    ------
    translated list: translated tokens.
    """
    text = np.array(text)
    words_not_O = text[np.where(text[:,1] != 'O')[0]]
    words = '@/*-+. '.join(words_not_O[:,0])
    trans = translate(words, to_language='en', from_language='pt')
    trans = trans.replace(' ', '')
    return np.concatenate((np.array(trans.split('@/*-+.')).reshape(-1,1), words_not_O[:,2].reshape(-1,1)), axis=1)

def removing_stopwords(tokens: list):
    """ 
    function that removes the stop-words.

    Parameters
    ----------
    tokens list: clinical note's tokens.

    Return
    ------
    text_without_stopwords list: tokens without stop words.
    """

    text_without_stopwords = []
    for text in tokens:
        # load stopwords
        stop_words = stopwords.words("english")
        text1 = text[0].split()
        text1 = [w for w in text1 if not w in stop_words]
        text1 = " ".join(text1)
        text_without_stopwords.append([text1, text[1]])

    return text_without_stopwords

def removing_numbers(tokens: list):
    """ 
    function that removes numeric values from tokens.

    Parameters
    ----------
    tokens list: clinical note's tokens.

    Return
    ------
    tokens_without_numbers list: tokens without numbers.
    """

    tokens_without_numbers = []
    for idx in range(len(tokens)):
        tokens_without_numbers.append([re.sub(r'\d+', '', tokens[idx][0]), tokens[idx][1]])

    return tokens_without_numbers

def removing_one_size_tokens(tokens: list):
    """ 
    function that removes size 1 tokens.

    Parameters
    ----------
    tokens list: clinical note's tokens.

    Return
    ------
    filt_text list: tokens filtered.
    """

    filt_text = []
    for idx in range(len(tokens)):
        if len(tokens[idx][0]) > 1:
            filt_text.append([tokens[idx][0], tokens[idx][1]])

    return filt_text

def tokenizing_text(text: str):
    """ 
    function that tokenizes the text.

    Parameters
    ----------
    text str: clinical note.

    Return
    ------
    tokens list: list with clinical notes tokens.
    """

    texts = [tokenize.word_tokenize(text, language='portuguese')]
    return texts

def acronym(texts:str):

        pwd = os.getcwd()
        PATH = os.path.join(pwd, 'app', 'services', 'preprocessing','Siglas.csv')
        df = pd.read_csv(PATH)
        vocab_siglas = df['SIGLA'].tolist()
        dicionario_siglas = dict(zip(df.SIGLA,df.DESCRICAO))  
        tokens_with_acronyms = []
        for idx,text in enumerate(texts[0]):
            if text.upper() in vocab_siglas:
               tokens_with_acronyms.extend(dicionario_siglas[text.upper()].lower().split())

            else:
                tokens_with_acronyms.append(texts[0][idx].lower())
        return ' '.join(tokens_with_acronyms)

def is_all_ner_O(ner: list):
    """ 
    checks if all NERs are equal to O. If they are, then it returns
     true and the code will not execute the following processing steps.

    Parameters
    ----------
    tokens list: NERs founded.

    Return
    ------
    bool: True if the NER list countain only O. 
    """

    set_ner = set(ner[0])
    if len(set_ner) <= 1:
        if list(set_ner)[0] == 'O':
            return True
        else:
            return False
    else:
        return False
from pandas import DataFrame
from numpy import inner, array, max, insert, where

from app.engine import db_interface
from app.engine import semantic_attribution


def embed(input):
    """ 
    function that calculates the embeddings 
    from a given string list.

    Parameters
    ----------
    input list: list of strings provided.
    
    Return
    ------
    embedds list: list of embeddings for each string.
    """
    
    return db_interface.model(input)

def correlation(message: list):
    """ 
    function that calculates the 
    correlation of strings from a list of strings.
    given a list of strings, the function calculates 
    the correlations of list[0] with all other list[1...n] strings.

    Parameters
    ----------
    message list: list of strings provided.
    
    Return
    ------
    corr list: list with the string correlations.
    """
    
    embeddings_ = embed(message)
    corr = inner(embeddings_, embeddings_)[0,:]
    return corr

def get_all_concepts_each_token(phrases_tokens: list):
    """ 
    function that returns all concepts, top concepts, 
    from a list of given clinical terms.

    Parameters
    ----------
    phrases_tokens list: list of clinical terms provided.
    
    Return
    ------
    snomed_terms_concepts list: list with the concepts, top concepts.
    """

    result = []
    for term in phrases_tokens:
        try:
            messages = []
            messages = semantic_attribution.search_in_snomed(term[0].split()) #_low_memory

            if type(messages[0]) == int:
                result.append(
                    [list(messages), 
                    semantic_attribution.maping_snomed_icd10(messages[0]), 
                    semantic_attribution.get_icpc_id(messages[0]),
                    term[1]])
            else:
                total = correlation(insert(messages[:,1], 0, term[0]))[1:]
                idx = where(array(total) == max(total))
                snomed_term = messages[idx[0][0]]
                result.append(
                    [list(snomed_term), 
                    semantic_attribution.maping_snomed_icd10(messages[0]),
                    semantic_attribution.get_icpc_id(messages[0]), 
                    term[1]])
        except Exception:
            result.append([['null', 'null'], ['null', 'null'], ['null'], term[1]])
    return result

def mount_output(grouped_tokens: list, result_get_snomed: list):
    """ 
    function that organizes the output to be displayed in the api. 
    It groups the tokens, NERs, snomed concepts in a single dataframe

    Parameters
    ----------
    grouped_tokens list: list containing the clinical note tokens and NERs.
    result_get_snomed list: list containing the named concepts.
    
    Return
    ------
    thina_str DataFrame: DF containing the grouped information.
    """
    
    thina_str = {'token': [],
             'ner': [],
             'snomed concept': [],
             'icd10':  [],
             'icpc(ciap)': []}

    for i, j in enumerate(grouped_tokens): # removing index
        grouped_tokens[i].pop(2)

    for i in result_get_snomed:
        grouped_tokens[int(i[-1])].extend(i[:3]) #insert the snomed_id, ICP and CIAP finded into grouped_tokens

    complement = [['null', 'null'], ['null', 'null'], ['null']]
    for idx, item in enumerate(grouped_tokens):
        try:
            access = grouped_tokens[idx][3]
        except Exception: 
            grouped_tokens[idx].extend(complement)

    grouped_tokens = array(grouped_tokens, dtype=object).T

    thina_str['token'] = grouped_tokens[0]
    thina_str['ner'] = grouped_tokens[1]
    thina_str['snomed concept'] = grouped_tokens[2]
    thina_str['icd10'] = grouped_tokens[3]
    thina_str['icpc(ciap)'] = grouped_tokens[4]

    return DataFrame(thina_str)
import re
import numpy as np
from app.engine import db_interface
from app.services.Assigning_id_concepts import get_concept

def check_number_in_str(my_string):
    """ 
    Checks if there are numbers in a string.

    Parameters
    ----------
    my_string str: String.
    
    Return
    ------
    term_concept_id list: positions of all number in the string
    """

    RE_D = re.compile('\d')
    return RE_D.search(my_string)

def prepare_icpc_terms(sample):
    """ 
    Prepares the relevant ICPC 
    table data so that it can be 
    processed and used to semantically 
    find the ICPC codes of a clinical note.

    Parameters
    ----------
    sample list: ICPC dataset`s row.
    
    Return
    ------
    phrase list: Al phrases that characterizes this row
    """

    index_terms = []
    inclusion = []
    try:
        inclu = sample['Inclusion'].split(';')
    except:
        inclu = ['']

    for text in inclu:
        idx = text.rfind(' ')
        if check_number_in_str(text[idx:]) is None:
            inclusion.append(text)
        else:
            inclusion.append(text[:idx])
    try:
        index_terms.extend(sample['Index terms'].split(';'))
    except:
        index_terms.append('')
    # index_terms.extend(sample['Index terms'].split(';'))
    phrase = []
    phrase.extend([sample['term']])
    phrase.extend(index_terms) 
    phrase.extend(inclusion)
    
    return phrase

def get_icpc_id(snomed_id = '000000'):
    """ 
    Returns the ICPC code (CIAP) of a clinical term, if any.

    Parameters
    ----------
    term string: Clinical term.
    
    Return
    ------
    code list: ICPC code
    """
    icpc_id = ['']
    icpc_snomed = db_interface.icpc[['SNOMED CT']].values

    if type(snomed_id) is int:
        snomed_id = str(snomed_id)
    elif type(snomed_id) is not int:
        snomed_id = str(snomed_id[0])

    for idx, id in enumerate(icpc_snomed):
        if snomed_id in id[0].split('; '):
            icpc_id = [db_interface.icpc.iloc[idx]['ICPC-3']]
            break
        else:
            icpc_id = ['null']

    return icpc_id

def search_in_snomed(term: list):
    """ 
    a function that returns the term and 
    conceptId present in snomed for a given clinical term.

    Parameters
    ----------
    term list: a list containing the clinical terms that 
    will be searched for in snomed.
    
    Return
    ------
    term_concept_id list: list containing all concepts
    found in snomed for the given term.
    """

    # phrases_tokens = ['heart', 'attack']

    limit = len(term)
    search_term = ' '.join(term)
    df = db_interface.dfs[limit]   
    result = df.query('term == @search_term')
    
    if len(result) > 0:
        return result.values[0][:2]
    else:
        
        search0 = 'term.str.contains(@term[0], na=False, case=False)'

        for i in range(1,len(term)):
            search = 'or term.str.contains(@term[@i], na=False, case=False)'
            search0 += search
        
        result = df.query(search0) 
        return result.values[:, :2]

def search_in_snomed_low_memory(term: list):
    """ 
    a function that returns the term and 
    conceptId present in snomed for a given clinical term. 
    This function use low memory, but the accuracy is very low.

    Parameters
    ----------
    term list: a list containing the clinical terms that 
    will be searched for in snomed.
    
    Return
    ------
    term_concept_id list: list containing all concepts
    found in snomed for the given term.
    """

    result = db_interface.df_descr.query('term == @search_term')
    if len(result) > 0:
        return result.values[0][:2]
    else:
        return ['null', 'null']

# def get_top_concept(conceptId=None):
    # """ 
    # A function that returns the top hierarchical conceptId 
    # in snomed by giving a clinical term.

    # Parameters
    # ----------
    # conceptId str: a string containing a numeric value.
    # conceptTerm str: a string containing a clinical term (in english).
    
    # Return
    # ------
    # top_term_concept list: list containing the highest concepts in the hierarchy in snomed.
    # """
    # top_term_concept = []

    # try:        
    #     if conceptId is not None:
    #         concept_id = conceptId

    #         while True:
    #             list_destination_id = db_interface.df_rela.query('sourceid == @concept_id and typeid == 116680003')['destinationid'].values
    #             if len(list_destination_id) == 0:
    #                 break
    #             else:
    #                 concept_id = list_destination_id[0]
    #             term_concept_id = db_interface.df_descr.query('conceptid == @concept_id')[['conceptid', 'term']].values[0]

    #             top_term_concept.append(term_concept_id)
    #         return list(top_term_concept[-2])
    # except Exception:
    #     return ['null', 'null']

def maping_snomed_icd10(concept_id: int):
    """ 
    maps snomed code to the ICD-10 database.

    Parameters
    ----------
    concept_id int: Snomed code.
    
    Return
    ------
    code str: ICD-10 code
    """

    try:
        if type(concept_id) is int:
            icd_code = db_interface.mapa.query('referencedComponentId == @concept_id').mapTarget[0]
            icd_term_code = list(db_interface.icd.query('code == @icd_code').values[0])
        elif type(concept_id) is not int:
            concept_id = concept_id[0]
            icd_code = db_interface.mapa.query('referencedComponentId == @concept_id').mapTarget[0]
            icd_term_code = list(db_interface.icd.query('code == @icd_code').values[0])
        else:
            icd_term_code = ['null', 'null']
    except Exception:
        icd_term_code = ['null', 'null']
    return icd_term_code

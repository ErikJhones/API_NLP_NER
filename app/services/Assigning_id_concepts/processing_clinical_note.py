import pandas as pd
from app.engine import constants
from app.services.Assigning_id_concepts import ner
from app.services.Assigning_id_concepts import get_concept
from app.services.Assigning_id_concepts import preprocessing_text
import time

def run_clinical_text_processing(text: str):
    inicio = time.time()
    """ 
    function that calculates the NER for each 
    token of a given clinical note.

    Parameters
    ----------
    sentencas list: a list containing the clinical terms.

    MODEL_DIR str: biobert's model path.
    
    Return
    ------
    output dict: dictionary containing the tokens, ners, 
    snomed_term, and snomed_top_term.
    """
    
    try:
        inicio = time.time()
        if len(text) <=1 :
            return {}
        else:
                
            word = preprocessing_text.removing_html_noise(
                text.lower()
            )
            
            word = preprocessing_text.tokenizing_text(
                word
            )
            
            my_ner = ner.predictBERTNER(
                word, 
                constants.PATH_NER
            )
            
            grouped_text = preprocessing_text.group_word_by_ner(
                word, 
                my_ner
            )

            if preprocessing_text.is_all_ner_O(my_ner):
                return {}
            else:
                no_date_text = preprocessing_text.filtring_dates(
                    group_text = grouped_text
                )
                
                translated_text = preprocessing_text.translating(
                    no_date_text
                )
                
                numbers_removed_text = preprocessing_text.removing_numbers(
                    translated_text
                )
                
                stop_words_removed_text = preprocessing_text.removing_stopwords(
                    numbers_removed_text
                )
                
                filtered_text = preprocessing_text.removing_one_size_tokens(
                    stop_words_removed_text
                )
                
                snomed_term_concepts = get_concept.get_all_concepts_each_token(
                    filtered_text
                ) 

                output = get_concept.mount_output(
                    grouped_tokens=no_date_text, 
                    result_get_snomed=snomed_term_concepts
                )

                fim = time.time()
                print(f"total time execution: {fim - inicio}")
                
                return output.reset_index(drop=True).to_json()
    except:
        return {}
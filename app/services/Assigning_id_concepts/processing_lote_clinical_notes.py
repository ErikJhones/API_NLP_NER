from app.services.Assigning_id_concepts import processing_clinical_note
import json
from os.path import join
import gc

def processing_notes(notes: dict) -> dict:
    """ 
    This function takes each clinical note and submits it to semantic processing.

    Parameters
    ----------
    input dict: A lot of clinical notes string.
    
    Return
    ------
    semantic dict: All clinical notes semantically processed.
    """
    
    
    for key, note in notes.items():
        output = {}
        output[key] = processing_clinical_note.run_clinical_text_processing(note)
        with open(join('app', 'output_NER_snomed', 'output_ner_snomed_'+str(key)+'.json'), 'w') as f:
            json.dump(output, f, ensure_ascii=False)
            
        gc.collect()

    return output
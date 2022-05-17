from json import load
from fastapi import APIRouter
from fastapi import File, UploadFile
from app.services.Assigning_id_concepts import processing_lote_clinical_notes
from app.services.delete_and_get import delete_and_get_file

router = APIRouter()
@router.post("/route_name_entity/", tags=["route name entity"])
async def create_upload_files(upload_file: UploadFile = File(...)) -> dict:
    """ 
    Route responsible for processing several clinical notes simultaneously. 
    The user must load a json file containing the patient's cpfs in its 
    indexes and the clinical notes in its elements.  

    To access the files with the notes processed by this route, enter the 
    /app/output_NER_snomed folder, it will contain all the outputs in json format.

    Parameters
    ----------
    json containing the cpf-indexed clinical notes
    
    Return
    ------
    json_processed json: A empty json file. Please use the route_get_output to
    access the output ner files.
    """


    json_data = load(upload_file.file)
    json_processed = processing_lote_clinical_notes.processing_notes(json_data)
    
    output = delete_and_get_file.get_files()
    return output
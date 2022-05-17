from fastapi import APIRouter
from fastapi import File, UploadFile
from app.services.delete_and_get import delete_and_get_file
 
router = APIRouter()
@router.post("/delete_output_ner/", tags=["delete  output NER"])
async def delete_output_ner() -> dict:
    """ 
    Route responsible for deleting the files in the folder ./app/output_NER_snomed.  

    It is important to call this route whenever processing a clinical note 
    to clear memory and remove unnecessary stored files.  

    Parameters
    ----------
    
    Return
    ------
   
    """
    
    delete_and_get_file.delete_files()
    return {}
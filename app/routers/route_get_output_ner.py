from fastapi import APIRouter
from fastapi import File, UploadFile
from app.services.delete_and_get import delete_and_get_file

router = APIRouter()
@router.post("/get_output_ner/", tags=["get  output NER"])
async def get_output_ner() -> dict:
    """ 
    Route responsible for providing the output in json 
    format of the entity naming function.  

    Parameters
    ----------
    
    Return 
    ------
    output json: A json file containing all clinical notes processed
    """

    output = delete_and_get_file.get_files()
    return output
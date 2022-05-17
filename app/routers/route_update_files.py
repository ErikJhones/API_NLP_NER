from fastapi import APIRouter
from typing import Optional
# from pydantic import BaseModel
from app.services.update_file import service_update_file
from typing import Optional
from fastapi import Query

router = APIRouter()

@router.post("/update_files_by_filter/", tags=["update files by filter"])
async def update(link: Optional[str] = Query('download link', min_length=1), file_name: Optional[str] = Query('ciap', min_length=11)):
    """
    Endpoint responsible for updating the files like models and datas. The user need to pass
    the download link and the kind of file to update (like data, or model) and the name.  
    
    Parameters  
    ----------
    
    link str: The google drive link of the file
    file_name str: The name of the file to be updated:  
    `ciap`, `cid`, `mapa`, `desc_snomed`, `rela_snomed`, `biobert`, `encoder`.  

    Return  
    ------
    The result of this operation is an Nx2 matrix. 
    It will be used to display the cluster graph.  
    """
    
    service_update_file.downloading(file_name, link)
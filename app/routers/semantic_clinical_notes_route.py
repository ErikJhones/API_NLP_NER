from fastapi import APIRouter
from typing import Optional
from app.services.Assigning_id_concepts import processing_clinical_note
from fastapi import Query

router = APIRouter()

@router.post("/assigning_snomed_concepts/", tags=["assigning snomed concepts"])
async def get_snomed_concepts(text: Optional[str] = Query('Clinical Note', min_length=1), cpf: Optional[str] = Query('00000000000', min_length=11)) -> dict:
    """
    Assigning snomed id_concepts in the clinical terms of a clinical note.
    """
    
    text_and_ner = processing_clinical_note.run_clinical_text_processing(text)
    return {cpf: text_and_ner.to_dict()}
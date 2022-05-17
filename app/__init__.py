from fastapi import FastAPI
from app.routers import route_name_entity
from app.routers import route_update_files
# from app.routers import route_get_output_ner
from app.routers import route_delete_outputs

app = FastAPI()

app.include_router(routers.router)
app.include_router(route_name_entity.router)
app.include_router(route_update_files.router)
# app.include_router(route_get_output_ner.router)
app.include_router(route_delete_outputs.router)
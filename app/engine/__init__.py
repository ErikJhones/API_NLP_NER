from app.engine.interface import DBInterface
from app.engine import import_files

import_files.importing_files()
db_interface = DBInterface()
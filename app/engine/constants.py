import os
from pathlib import Path

pwd = os.getcwd()
PATH_DATA = os.path.join('app', 'data')
PATH_MODEL = os.path.join('app', 'model')
PATH_NER = os.path.join(PATH_MODEL, 'biobert-all-clinpt/')
import os
import wget
import gdown
import zipfile
import tarfile
import shutil

from app.engine import constants

def update(file_name, url_file, directory):
    os.remove(os.path.join(directory, file_name))
    url = url_file
    output = os.path.join(directory, file_name)
    gdown.download(url, output, quiet=False)

def downloading(file_name, url_file):
    if file_name == 'ciap':
        update('ICPC3.csv', url_file, constants.PATH_DATA)

    elif file_name == 'cid':
        update('icd_10_codes_2022.csv', url_file, constants.PATH_DATA)
    
    elif file_name == 'mapa':
        update('mapa_snomed_idc10.csv', url_file, constants.PATH_DATA)

    elif file_name == 'desc_snomed':
        update('description_snomed.csv', url_file, constants.PATH_DATA)

    elif file_name == 'rela_snomed':
        update('relationship_snomed.csv', url_file, constants.PATH_DATA)
    
    elif file_name == 'biobert':
        directory = constants.PATH_MODEL
        shutil.rmtree(os.path.join(directory, 'biobert-all-clinpt'))

        output = 'biobert-all-clinpt.zip'
        gdown.download(url_file, output, quiet=False)

        with zipfile.ZipFile('biobert-all-clinpt.zip', 'r') as zip_ref:
            zip_ref.extractall(directory)

        os.remove('biobert-all-clinpt.zip')

    elif file_name == 'encoder':
        directory = constants.PATH_MODEL
        shutil.rmtree(os.path.join(directory, 'universal-sentence-encoder_4'))
        wget.download(url_file)

        with tarfile.open('universal-sentence-encoder_4.tar.gz') as file:
            file.extractall(os.path.join(directory, 'universal-sentence-encoder_4'))

        os.remove('universal-sentence-encoder_4.tar.gz')
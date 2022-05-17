# downloading and import models and files necessaries for the project

import os
import wget
import gdown
import zipfile
import tarfile
from pathlib import Path

def importing_files():
    fileName = os.path.join('app', 'output_NER_snomed')
    fileObj = Path(fileName)
    
    if not fileObj.is_dir():
        os.mkdir(os.path.join('app',  'output_NER_snomed'))


    fileName = os.path.join('app', 'model')
    fileObj = Path(fileName)
    
    if not fileObj.is_dir():
        os.mkdir(os.path.join('app',  'model'))
    
    fileName = os.path.join('app', 'model', 'biobert-all-clinpt')
    fileObj = Path(fileName)

    if not fileObj.is_dir():
        print('******************************************************')
        print('Downloading files....')

        # download biobert model for NER
        url = 'https://docs.google.com/uc?export=download&id=1r29Zh5IVJZHuILwQOB8OU_9jcFR3yXJb'
        output = 'biobert-all-clinpt.zip'
        gdown.download(url, output, quiet=False)

        with zipfile.ZipFile('biobert-all-clinpt.zip', 'r') as zip_ref:
            zip_ref.extractall(os.path.join('app',  'model'))

        os.remove('biobert-all-clinpt.zip')

    # download tensorflow sentence encoder model
    fileName = os.path.join('app', 'model', 'universal-sentence-encoder_4')
    fileObj = Path(fileName)
    
    if not fileObj.is_dir():
        os.mkdir(os.path.join('app',  'model', 'universal-sentence-encoder_4'))
        wget.download('https://tfhub.dev/google/universal-sentence-encoder/4?tf-hub-format=compressed')

        with tarfile.open('universal-sentence-encoder_4.tar.gz') as file:
            # file = tarfile.open('universal-sentence-encoder_4.tar.gz')
            file.extractall(os.path.join('app',  'model', 'universal-sentence-encoder_4'))
            # file.close()

        os.remove('universal-sentence-encoder_4.tar.gz')

    # download data like snomed, cid-10, mapp-cid-10, ciap

    fileName = os.path.join('app',  'data')
    fileObj = Path(fileName)
    if not fileObj.is_dir():
        url = 'https://docs.google.com/uc?export=download&id=1XhKBbhiZfRcVl9VLoq6_85ATgEpvP23t'
        output = 'data.zip'
        gdown.download(url, output, quiet=False)
		
        with zipfile.ZipFile('data.zip', 'r') as zip_ref:
            zip_ref.extractall(os.path.join('app'))

        os.remove('data.zip')

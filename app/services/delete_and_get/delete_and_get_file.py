from os import walk, remove
from os.path import join
from json import dump, load

def delete_files():
    '''
    
    '''
    path = join('app', 'output_NER_snomed')
    for caminho, d, file in walk(path):
        for filename in file:
            remove(join(path, filename))

def get_files():
    '''
    '''
    output = {}
    path = join('app', 'output_NER_snomed')

    for caminho, d, file in walk(path):
        for filename in file:
            with open(join(path, filename), "r") as jsonFile:
                data = load(jsonFile)
            output.update(data)
    return output
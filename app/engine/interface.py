import pandas as pd
import numpy as np
from app.engine import constants
from os import path
import tensorflow as tf
import os

class DBInterface:
    """Provides a more friendly interface to the main databases used by the project."""
    def __init__(self):
        self.path_snomed = constants.PATH_DATA
        self.dfs = []
        self.df_descr = []
        # self.df_rela = []
        self.mapa = []
        self.icd = []
        self.model = self.loading_model()
        self.icpc = []

        self.loading_dataframes()

    def loading_model(self):
        return tf.keras.models.load_model(os.path.join(constants.PATH_MODEL, 'universal-sentence-encoder_4'))

    def loading_dataframes(self):
        # relationship
        # self.df_rela = pd.read_csv(path.join(self.path_snomed, 'relationship_snomed.csv'), usecols=['sourceid', 'destinationid', 'typeid'])
        
        # description
        self.df_descr = pd.read_csv(path.join(self.path_snomed, 'description_snomed.csv'), usecols=['term', 'conceptid', 'active']).query('active == 1')
        self.df_descr['total'] = self.df_descr['term'].str.split().str.len()
        self.df_descr['term'] = self.df_descr['term'].str.lower()
        self.df_descr.drop(['active'], axis=1,inplace=True)

        for i in range(int(self.df_descr.total.max())):
            self.dfs.append(self.df_descr.query('total == @i'))
        
        # maping snomed icd10
        self.mapa = pd.read_csv(path.join(self.path_snomed, 'mapa_snomed_idc10.csv'), usecols=['referencedComponentId', 'mapTarget']) 
        self.mapa.dropna(inplace=True)

        # ICD10
        self.icd = pd.read_csv(path.join(self.path_snomed, 'icd_10_codes_2022.csv'))
        codes = []
        for i in self.icd['code']:
            if len(i) > 3:
                cod = i[:3] + '.' + i[3:]
                codes.append(cod)
            else:
                codes.append(i)
        self.icd['code'] = codes

        # ICPC
        self.icpc = pd.read_csv(path.join(self.path_snomed, 'ICPC3.csv'), usecols=['ICPC-3', 'SNOMED CT'])
        self.icpc.fillna(';', inplace=True)

        del(self.df_descr)
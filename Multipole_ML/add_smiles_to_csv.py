import os
import pandas as pd
from pubchempy import get_cids,get_compounds
import re
import time

current_dir = os.path.dirname(os.path.realpath('__file__'))

raw_data_file = os.path.join(current_dir, './electrolyte_data.dat')
raw_data_csv = pd.read_csv(raw_data_file)

raw_data = raw_data_csv.iloc[:,[0,1,2,3,4,5]]

raw_data.columns = ['material', 'Li','Na','K','Rb','Cs']

materials = raw_data['material'].values

ion_replacements = {
     'HBr': ' hydrobromide',
     '2Br': ' dibromide',
     'Br': ' bromide',
     'HCl': ' hydrochloride',
     '2H2O': ' dihydrate',
     'H20': ' hydrate',
     'Na': ' sodium'
}

ion_keys = ['H20', 'HBr', 'HCl', '2Br', '2H2O', 'Br', 'Na']

def compound_to_smiles(cmpd):
    try:
        compound = re.sub(r'([^\s\w]|_)+', '', cmpd)
        for ion in ion_keys:
            if ion in compound:
                 compound = compound.replace(ion,ion_replacements[ion])    
        time.sleep(7) #so pubchem doesnt get mad at the number of requests
        cid = get_cids(compound, 'name')[0]
        smiles = get_compounds(cid)[0].canonical_smiles
        return smiles
    except IndexError as error:
        try:
            cmpnd = get_compounds(cmpd,'name')[0]
            smiles = get_compounds(cmpnd.cid)[0].canonical_smiles   
            return smiles
        except IndexError as error:
            return "NaN"

smiles_map = {}

for i in materials:
    smiles_map[i] = compound_to_smiles(i)

smiles_data = raw_data
smiles_data['material'] = smiles_data['material'].apply(lambda x: smiles_map[x])

smiles_data.to_csv('output_test.csv')

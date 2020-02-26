import deepchem as dc

dataset_file = 'test.csv'
task = ['surface_tension']
featurizer_func = dc.feat.ConvMolFeaturizer()

loader = dc.data.CSVLoader(tasks=task, smiles_field='smiles', featurizer=featurizer_func)
dataset = loader.featurize(dataset_file)


transformer = dc.trans.NormalizationTransformer(transform_y=True,dataset=dataset)
dataset = transformer.transform(dataset)


dc.utils.save.save_to_disk(dataset, 'balanced_dataset.joblib')
balanced_dataset = dc.utils.save.load_from_disk('balanced_dataset.joblib')

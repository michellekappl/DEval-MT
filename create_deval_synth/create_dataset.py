import pandas as pd
import re

dataset = pd.read_csv('dataset_old.txt', names = ["sentence", "hierarchy", "group_x", "group_y"], sep = ";")
nan_val = dataset[dataset['group_y'].isna()]

if not nan_val["group_x"].isna().all():
    dataset.loc[nan_val.index, "group_x"] = "[]"
    dataset.loc[nan_val.index, "group_y"] = "[]"

dataset.loc[dataset['hierarchy'].str.contains(r'\[|\]', na=False), 'hierarchy'] = "none"
dataset.loc[dataset['group_x'].str.contains(r'\[none\]', na=False), 'group_x'] = "none"
#dataset.loc[dataset['hierarchy'].str.contains(r'unklar', na=False), 'hierarchy'] = None
#dataset.loc[dataset['hierarchy'].str.contains(r'x=y', na=False), 'hierarchy'] = None
dataset.loc[dataset['group_x'].str.contains(r'^(?!.*x_).+$', na=False), 'group_x'] = "[]"
dataset.loc[dataset['group_y'].str.contains(r'^(?!.*y_).+$', na=False), 'group_y'] = "[]"

dataset = dataset.replace({pd.NA: None})

dataset.to_csv('dataset.csv', index=False, encoding='utf-8', sep=';')
#!/usr/bin/env python
import time
import platform

import numpy as np
import sys

if len(sys.argv) > 1:
    print("import boa vista xgboost")
    import cythonize_xgboost as xgb
else:
    print("import default xgboost")
    import xgboost as xgb
import numpy as np
from sklearn.datasets import make_regression

# xgb.set_config(verbosity=2)


def test_xgb_regression(n_samples = 10000, n_features = 20, n_estimators = 3, depth = 11):
    # dicionario de estatistica que posteriormente sera csv
    stats = {}
    stats["so"] =  platform.system()
    stats["n_samples"] =  n_samples
    stats["n_features"] =  n_features
    stats["n_estimators"] =  n_estimators
    stats["depth"] =  depth

    #creating dataset
    start = time.time()
    x, y = make_regression(n_samples = n_samples, n_features = n_features, n_informative = n_features - 1, random_state = 1)
    stats["make_regression"] = time.time() - start
    
    #training xgb classifier on random dataset
    def create_xgb():
        
        start = time.time()
        model = xgb.XGBRegressor(max_depth = depth, learning_rate = 0.1, n_estimators = n_estimators,
                                 objective = 'reg:squarederror', n_jobs = 8, min_child_weight = 1, 
                                  subsample = 0.8, colsample_bytree = 0.8,
                                  random_state = 5, missing = np.nan,
                                  base_score = 0.5)
        stats["xgb.XGBRegressor"] = time.time() - start

        start = time.time()
        model.fit(x, y)
        stats["model.fit"] = time.time() - start

        return model

    start = time.time()
    model = create_xgb()
    stats["create_xgb"] = time.time() - start
    
    start = time.time()
    booster = model.get_booster()
    stats["model.get_booster"] = time.time() - start

    start = time.time()
    tree_data = booster.get_dump(dump_format='json')
    stats["booster.get_dump"] = time.time() - start

    start = time.time()
    for i in range(len(tree_data)):
        f = open("trees/tree_%d.json" % i, 'w')
        f.write(tree_data[i])
        f.close()
    stats["open_trees"] = time.time() - start

    stats["% model.fit"] = stats["model.fit"] / stats["create_xgb"]

    return stats

if __name__ == "__main__":
    # test_xgb_regression(
    #     n_samples=10000, n_features=20, n_estimators=200, depth=10
    # )

    import csv
    import sys
    import copy

    count = 0
    max_iterations = 5
    stats_keys = ['so', 'n_samples', 'n_features', 'n_estimators', 'depth',
            'make_regression', 'xgb.XGBRegressor', 'model.fit', 'create_xgb',
            'model.get_booster', 'booster.get_dump', 'open_trees', 
            '% model.fit'
    ]
    col_num  = len(stats_keys)
    pos_col_model_fit = 7
    data = []

    writer = csv.DictWriter(sys.stdout, fieldnames=stats_keys, delimiter=';')
    while count < max_iterations:
        stats = test_xgb_regression(
            n_samples=10000, n_features=20, n_estimators=100, depth=10
        )
        data.append(stats)
        count += 1

    min = min([d[stats_keys[pos_col_model_fit]] for d in data])
    max = max([d[stats_keys[pos_col_model_fit]] for d in data])
    avg = sum([d[stats_keys[pos_col_model_fit]] for d in data]) / len(data)

    resul_dict = copy.deepcopy(data[0])
    resul_dict[stats_keys[0]] = "Resultado"
    for key in stats_keys[1:]:
        resul_dict[key] = None
    data.append(resul_dict)

    resul_dict = copy.deepcopy(data[0])
    resul_dict[stats_keys[0]] = "Min"
    for i, key in enumerate(stats_keys):
        if i == 0:
            continue
        elif i == pos_col_model_fit:
            resul_dict[key] = min 
        else:
            resul_dict[key] = None
    data.append(resul_dict)

    resul_dict = copy.deepcopy(data[0])
    resul_dict[stats_keys[0]] = "Max"
    for i, key in enumerate(stats_keys):
        if i == 0:
            continue
        elif i == pos_col_model_fit:
            resul_dict[key] = max 
        else:
            resul_dict[key] = None
    data.append(resul_dict)
    resul_dict = copy.deepcopy(data[0])
    resul_dict[stats_keys[0]] = "Avg"
    for i, key in enumerate(stats_keys):
        if i == 0:
            continue
        elif i == pos_col_model_fit:
            resul_dict[key] = avg
        else:
            resul_dict[key] = None
    data.append(resul_dict)

    for d in data:
        for i, key in enumerate(stats_keys):
            if i > 4 and d[key] != None and type(d[key]) != str:
                d[key] = "%.4f" % d[key]
                d[key] = d[key].replace('.',',')

    for d in data:
        writer.writerow(d)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

n_rep = 10
def clean_res(res, data_type='classification'):
    res = pd.DataFrame(res)
    res['objective_name'] = res['objective_name'].replace('FairSVM[C=1.0,obj=1,rho=0.01]', 'FairSVM-obj')
    res['objective_name'] = res['objective_name'].replace('FairSVM[C=1.0,obj=0,rho=0.01]', 'FairSVM-C')
    res = res.replace({'solver': r'\[.*.='}, {'solver': '['}, regex=True)
    res = res.replace({'objective_name': r'\[.*.\]'}, {'objective_name': ''}, regex=True)

    if data_type == 'classification':
        dataset_lst = ['steel-plates-fault', 'philippine', 'sylva_prior', 'creditcard']
    else:
        dataset_lst = ['liver-disorders', 'kin8nm', 'house_8L', 'topo_2_1', 'Buzzinsocialmedia_Twitter']
    # for col_tmp in ['data_name', 'solver']:
    for col_tmp in ['data_name']:
        res = res.replace({col_tmp: r'.*.*\='}, {col_tmp: ''}, regex=True)
        res = res.replace({col_tmp: r'\]'}, {col_tmp: ''}, regex=True)
    
    res.data_name = pd.Categorical(res.data_name, categories=dataset_lst)
    return res

eps = 1e-5
pd.reset_option('display.float_format')
res = {'objective_name': [], 
        'data_name': [], 
        'solver': [], 
        'if_solve': [],
        'time': []}

for file_name in ['./benchmark_FairSVM/outputs/benchopt_run_2023-10-12_22h11m38.parquet', 
                  './benchmark_Huber/outputs/benchopt_run_2023-10-10_22h40m00.parquet', 
                  './benchmark_QR/outputs/benchopt_run_2023-10-14_22h48m25.parquet', 
                  './benchmark_sSVM/outputs/benchopt_run_2023-10-10_20h52m22.parquet',
                  './benchmark_SVM/outputs/benchopt_run_2023-10-10_20h12m15.parquet']:
    
    obj_tmp = file_name.split('/')[1]
    if obj_tmp in ['benchmark_FairSVM', 'benchmark_sSVM', 'benchmark_SVM']:
        data_type = 'classification'
    else:
        data_type = 'regression'

    # df = pd.read_csv(file_name)
    df = pd.read_parquet(file_name)
    perf = {'idx_rep': [],
            'objective_name': [], 
            'data_name': [], 
            'solver': [], 
            'if_solve': [],
            'time': []}

    dataset_lst = set(df['data_name'])

    for obj_name in set(df['objective_name']):
        for data_name in set(df['data_name']):
            for solver in set(df['solver_name']):
                for idx_rep in range(n_rep):
                    if 'FairSVM' in file_name:
                        ## when FairSVM, we use ReHLine as optimal value, since the results provided by other methods may not feasible
                        opt_obj = min(df[(df['objective_name'] == obj_name) & (df['data_name'] == data_name) & (df['idx_rep'] == idx_rep) & (df['solver_name']=='rehline[shrink=True]')]['objective_value'])
                    else:
                        opt_obj = min(df[(df['objective_name'] == obj_name) & (df['data_name'] == data_name) & (df['idx_rep'] == idx_rep)]['objective_value'])
                    dt = df[(df['objective_name'] == obj_name) & (df['data_name'] == data_name) & (df['solver_name'] == solver) & (df['idx_rep'] == idx_rep)]
                    dt = dt[(dt['objective_value'] - opt_obj) < eps*np.maximum(dt['objective_value'], 1)]['time']
                    if len(dt) > 0:
                        time_tmp = min(dt)
                        
                        perf['idx_rep'].append(idx_rep)
                        perf['objective_name'].append(obj_name)
                        perf['data_name'].append(data_name)
                        perf['solver'].append(solver)
                        perf['time'].append(time_tmp)
                        # perf['std'].append(dt.std() / np.sqrt(len(dt)))
                        perf['if_solve'].append(True)

                        res['objective_name'].append(obj_name)
                        res['data_name'].append(data_name)
                        res['solver'].append(solver)
                        res['if_solve'].append(True)
                    else:
                        perf['idx_rep'].append(idx_rep)
                        perf['objective_name'].append(obj_name)
                        perf['data_name'].append(data_name)
                        perf['solver'].append(solver)
                        perf['time'].append(np.nan)
                        # perf['std'].append(np.nan)
                        perf['if_solve'].append(False)

                        res['objective_name'].append(obj_name)
                        res['data_name'].append(data_name)
                        res['solver'].append(solver)
                        res['time'].append(np.nan)
                        res['if_solve'].append(False)

    perf = clean_res(perf, data_type)

    psum = perf.groupby(['objective_name', 'solver', 'data_name'], as_index=False, observed=False).agg({'time': ['mean', 'std'], 'if_solve':['mean']})
    print(psum.to_markdown(floatfmt='.5f', index=False))
    print('\n')

    pp = perf.groupby(['objective_name', 'solver', 'data_name'], as_index=False, observed=False)['time'].mean()
    pp = pp.pivot(index=['objective_name', 'data_name'], columns='solver', values='time')

    for col_tmp in pp.columns:
        print('speed-up of rehline/%s: min: %.1f - max: %.1f' 
        %(col_tmp, np.nanmin(pp[col_tmp]/pp['rehline[True]']), np.nanmax(pp[col_tmp]/pp['rehline[True]'])))
    print('\n')    

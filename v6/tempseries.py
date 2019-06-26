import filterlog
from pandas import DataFrame
from numpy import pad, sort
from pprint import pprint


filterlog.gerar_csv_logIdeal()
filename = 'ideal_Prod1Torno2.csv'
path = './data/'
delimiter = ','


def fill_all_arr_dict(dataset_o):

    dataset = dataset_o.copy()

    max_size = max(len(x) for x in dataset.values())

    print(max_size)

    for item,s_name in zip(dataset.values(), dataset.keys()):
        if len(item) == max_size:
            continue
        else:
            dataset[s_name] = pad(item, [0, max_size - len(item)], mode='constant')
    
    return dataset


def trim_percentage(arr = [], leftp=0.05, rightp=0.05):

    arr_len = len(arr)
    new_arr = arr.copy()
    sorted_arr = sort(new_arr, kind='mergesort')
    deletees = []
    left_trim = leftp * arr_len
    right_trim = (1 - rightp) * arr_len

    for i in range(len(sorted_arr)):
        if i <= left_trim or i >= right_trim:
            deletees.append(sorted_arr[i])
        else:
            pass
    
    for item in deletees:
        new_arr.remove(item)

    return new_arr
    


def agrupar_series_temporais():

    series = dict()

    with open(path+filename) as f:

        f.__iter__().__next__()

        for line in f:
            line_arrr = line.split(delimiter)
            if not line_arrr[1] in series:
                series[line_arrr[1]] = [int(line_arrr[2])]
            else:
                series[line_arrr[1]].append(int(line_arrr[2]))

        f.close()

    for serie in series:
        series[serie] = trim_percentage(series[serie], .05, .3)
        
    
    series = fill_all_arr_dict(series)
    # series['Producao'] = trim_percentage(series['Producao'], .01, .09)
    # series = fill_all_arr_dict(series)

    x = [len(l) for l in series.values()]
    print(x)

    return series, series.keys()
    
series_temporais, colunas = agrupar_series_temporais()

df = DataFrame(series_temporais, columns=colunas)
df.index.name = "index"
df.to_csv(path + 'series_temporais.csv')
print("done")

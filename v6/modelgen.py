import pandas as pd
from pprint import pprint
from matplotlib import pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
import numpy as np

filename = 'series_temporais.csv'
path = './data/' 
delimiter = ','
df = pd.read_csv(path + filename, index_col="index")



def predictions_threshold(dataframe):
    return dataframe.shape[0]*0.005

def hold_out_value(table, pctg=0.7):
    a = round(length_no_zeros(table)*pctg)
    return a

def hold_out(dataframe):
    holdout = dataframe.copy()
    for column in dataframe:
        holdout[column] = dataframe[column][0:hold_out_value(dataframe[column])]


    return holdout.fillna(0)

def length_no_zeros(table):
    t = 0
    for value in table:
        if value == 0:
            break
        t += 1
        
    return t

#train model using exact maximum likelihood via Kalman filter.
def train_all_series(dataframe, atvs_interesse):

    models = pd.DataFrame(0, index=np.arange(len(dataframe)), columns=dataframe.columns)
    
    
    for column in dataframe:
        if length_no_zeros(dataframe[column]) > 12 and column not in atvs_interesse:
            #print()
            #model = ARIMA(np.log(dataframe[column]).replace([np.inf, -np.inf], np.nan).dropna(), order=(0,0,1))
            model = ARIMA(dataframe[column], order=(0,0,1))
            modelfit = model.fit(disp=False, trend='c')
            hdv = hold_out_value(dataframe[column])
            models[column] = modelfit.predict(start=hdv, end=length_no_zeros(dataframe[column])-1)
            
    
    #return (hold_out(dataframe) + np.exp(models).fillna(0))
    dfret = (hold_out(dataframe) + models.fillna(0)) 
    
    for column in atvs_interesse:
        dfret[column] = dataframe[column]
            
    return dfret


def definir_atividade_interesse(dataframe):
    
    atvs = []
    
    print('Atividades e seus respectivos numeros:')
    for i, atv in zip(range(dataframe.shape[1]), dataframe):
        print(atv + ' ' + str(i))
    
    print('Digite o numero da(s) atividade(s) de interesse')
    while(True):
        inp = input()
        if inp == '':
            break
        elif inp.isdigit():
            n = int(inp)  
            if n >= 0 and n < dataframe.shape[1]:
                atvs.append(dataframe.columns.values[n])
            else:
                raise Exception(str(n) + " nao esta registado como uma atividade")
        else:
                raise Exception(inp + " nao e uma atividade valida")
        
    return atvs


atvs_interesse = definir_atividade_interesse(df)
c = train_all_series(df, atvs_interesse)
f = lambda x: round(x) 
c = c.applymap(f)

print(c)
c.to_csv(path + 'predictions.csv', index=False)

for atv in atvs_interesse:
    l = length_no_zeros(df[atv]) - 1
    media = round(df[atv][0:l].mean())
    print(f'Media de {atv} {media}')
    

print("done")

import itertools as it
import pandas as pd

#Se crean las funciones de soporten necesarias:

def operation_pd(a, b):
    return b[:a]

#Toma vectores y regresa el promedio para cada ubicación. Ejemplo: toma [1,2,3,4] & [5,7,9] y regresa [3,4.5,6,4]
def aggr_avg(result_col):
    def avg(x):
        x = [i for i in x if i is not None]
        return sum(x, 0.0000)/len(x)
    filt = list(map(avg, it.zip_longest(*result_col)))
    return filt

#Toma vectores y regresa la suma para cada ubicación. Ejemplo: toma [1,2,3,4] & [5,7,9] y regresa [6,9,12,4]
def aggr_sum(result_col):
    def avg(x):
        x = [i for i in x if i is not None]
        return sum(x, 0.0000)
    filt = list(map(avg, it.zip_longest(*result_col)))
    return filt

#Toma vectores y regresa el recuento para cada ubicación. Ejemplo: toma [1,2,3,4] & [5,7,9] y regresa [2,2,2,1]
def aggr_count(result_col):
    def avg(x):
        x = [i for i in x if i is not None]
        return len(x)
    filt = list(map(avg, it.zip_longest(*result_col)))
    return filt

#Esta función permite encontrar la posición de un encabezado espeífico (a) en un dataframe (df)
def encontrar_encabezado(df,a):
    n=0
    for i in list(df):
        if str(i)==str(a):
            pos=n
            break
        n=n+1
    return pos

#Esta función devuelve todos los cortes. Es decir, todos los campos que inician con c_...
def all_cortes(df):
    temp = []
    for i in list(df):
        if str(i)[0:2]=='C_':
            temp.append(i)
    return temp

#Esta funcion lleva los valores de una lista a porcentaje. 0.05123456789 -> 5.1235
def porcentaje(resultado):
    resultado = [100*x for x in resultado]
    resultado = [round(x,4) for x in resultado]
    return resultado      

#Permite obtener el promedio ponderado
def weighted_average(df, data_col, weight_col):
    df['_data_times_weight'] = df[data_col] * df[weight_col]
    df['_weight_where_notnull'] = df[weight_col] * pd.notnull(df[data_col])
    result = df['_data_times_weight'].sum() / df['_weight_where_notnull'].sum()
    del df['_data_times_weight'], df['_weight_where_notnull']
    return result
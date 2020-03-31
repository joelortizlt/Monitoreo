import itertools as it

#Se crean las funciones de soporten necesarias
def operation_pd(a, b):
    return b[:a]

def aggr_avg(result_col):
    def avg(x):
        x = [i for i in x if i is not None]
        return sum(x, 0.0000)/len(x)
    filt = list(map(avg, it.zip_longest(*result_col)))
    return filt

def aggr_sum(result_col):
    def avg(x):
        x = [i for i in x if i is not None]
        return sum(x, 0.0000)
    filt = list(map(avg, it.zip_longest(*result_col)))
    return filt

#---

#Esta función permite encontrar la posición de un encabezado espeífico (a) en un dataframe (df)
def encontrar_encabezado(df,a):
    n=0
    for i in list(df):
        if str(i)==str(a):
            pos=n
            break
        n=n+1
    return pos

#Esta función devuelve todos los cortes (c_...)
def all_cortes(df):
    temp = []
    for i in list(df):
        if str(i)[0:2]=='c_':
            temp.append(i)
    return temp

#Esta funcion lleva los valores de una lista a porcentual
def porcentaje(resultado):
    resultado = [100*x for x in resultado]
    resultado = [round(x,4) for x in resultado]
    return resultado
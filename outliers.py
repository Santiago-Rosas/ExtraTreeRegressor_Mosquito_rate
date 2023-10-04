import pandas as pd
import numpy as np

#fucntions to detect and repalce or remove outliers 

## extract low limit and upper limit 
def outlier_thresholds(dataframe=pd.DataFrame, variable=str):
    quartile1 = dataframe[variable].quantile(0.05) ###in this case i will youse tyhsi values as a quartile becouse i dont want to loss to much info 
    quartile3 = dataframe[variable].quantile(0.95)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit.round(), up_limit.round()

##suum all outliers per feature

def sum_outliers(dataframe=pd.DataFrame, variable=str):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    lista = [i for i in dataframe[variable] if i < low_limit or i > up_limit]
    return len(lista)
            
 

##identifie the index of the outliers
def index_out_liers(dataframe, variable=str):
    index=[]
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    index.append(list(np.where((dataframe[variable] < low_limit) | (dataframe[variable] > up_limit))[0]))
    return index[0]

###create a table with the number of outliers per column 

def table_outliers(dataframe,features=list):
    out_layers= pd.DataFrame()
    for i in features: 
        lista= sum_outliers(dataframe, i)
        out_layers[i]= [lista]
        Outlayers=out_layers.T
        Outlayers.columns=["Number_outliers"]
    return Outlayers.sort_values(by="Number_outliers",ascending=False)


###remove all outliers from a df 

def remove_outliers_from_df(dataframe, variable=list)->pd.DataFrame:
    all_Out_layers=[]
    for i in variable:
        index=index_out_liers(dataframe, variable)
        for j in index:
            if j not in all_Out_layers:
                all_Out_layers.append(j)
        return dataframe.drop(dataframe.index[all_Out_layers])  
    


###replace out layers with low limit or up_limit 

def replace_with_thresholds(dataframe, variable=str):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

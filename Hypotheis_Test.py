# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
def get_list_of_university_towns():
    with open(r'university_towns.txt') as file:
        data = file.readlines()
    lst = []
    state = ''
    region = '' 
    for i in data:
        if '[ed' in i:
            state = i.split("[ed")[0]
        else:
            region = (i.split("(")[0]).strip()
            lst.append([state,region])
    df = pd.DataFrame(lst, columns=["State", "RegionName"])
    return df
    '''
    Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
        DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
                  columns=["State", "RegionName"]  )
        The following cleaning needs to be done:
            1. For "State", removing characters from "[" to the end.
            2. For "RegionName", when applicable, removing every character from " (" to the end.
            3. Depending on how you read the data, you may need to remove newline character '\n'. 
    '''
def get_recession_start():
    gdp = pd.read_excel(r'gdplev.xls',skiprows=7).drop(['Unnamed: 0','Unnamed: 1','Unnamed: 2','Unnamed: 3','Unnamed: 5','Unnamed: 7'], axis=1)
    gdp.columns = ['quarter','gdp']
    row = gdp[gdp['quarter']=='2000q1'].index[0]
    gdp = gdp.loc[row:,:].reset_index()
    gdp = gdp.set_index('quarter').drop(['index'], axis=1)
    gdp['gdpchange'] = gdp['gdp']-gdp['gdp'].shift(1)
    gdp['RecessionStart'] = (gdp['gdpchange'] < 0) & (gdp['gdpchange'].shift(-1) < 0)
    return gdp[gdp['RecessionStart'] == True].index[0]
    '''
    Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3
    '''
def get_recession_end():
    gdp = pd.read_excel(r'gdplev.xls',skiprows=7).drop(['Unnamed: 0','Unnamed: 1','Unnamed: 2','Unnamed: 3','Unnamed: 5','Unnamed: 7'], axis=1)
    gdp.columns = ['quarter','gdp']
    row = gdp[gdp['quarter']=='2000q1'].index[0]
    gdp = gdp.loc[row:,:].reset_index()
    gdp = gdp.set_index('quarter').drop(['index'], axis=1)
    gdp['gdpchange'] = gdp['gdp']-gdp['gdp'].shift(1)
    start = get_recession_start()
    gdp = gdp[gdp.index>=start]    
    gdp['RecessionEnd'] = (gdp['gdpchange'] > 0) & (gdp['gdpchange'].shift(+1) > 0)
    return gdp[gdp['RecessionEnd'] == True].index[0]
    '''
    Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3
    '''
def get_recession_bottom():
    gdp = pd.read_excel(r'gdplev.xls',skiprows=7).drop(['Unnamed: 0','Unnamed: 1','Unnamed: 2','Unnamed: 3','Unnamed: 5','Unnamed: 7'], axis=1)
    gdp.columns = ['quarter','gdp']
    row = gdp[gdp['quarter']=='2000q1'].index[0]
    gdp = gdp.loc[row:,:].reset_index()
    gdp = gdp.set_index('quarter').drop(['index'], axis=1)
    gdp['gdpchange'] = gdp['gdp']-gdp['gdp'].shift(1)
    start = get_recession_start()
    gdp = gdp[gdp.index>=start]    
    gdp['RecessionEnd'] = (gdp['gdpchange'] > 0) & (gdp['gdpchange'].shift(+1) > 0)
    end = gdp[gdp['RecessionEnd'] == True].index[0]
    gdp = gdp.loc[start:end,:]
    return gdp['gdp'].idxmin()
    '''
    Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3
    '''
def convert_housing_data_to_quarters():
    housing = pd.read_csv('City_Zhvi_AllHomes.csv')
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    housing['State'] = housing['State'].replace(states)
    housing = housing.set_index(['State','RegionName'])
    housing = housing.loc[:,'2000-01':'2016-08']
    housing.columns = pd.to_datetime(housing.columns)
    housing = housing.resample('Q',axis=1).mean()
    housing = housing.rename(columns=lambda x: str(x.to_period('Q')).lower())
    return housing
    '''
    Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
def run_ttest():
    rec_start=get_recession_start()
    rec_bottom = get_recession_bottom()
    hdf = convert_housing_data_to_quarters()
    ul = get_list_of_university_towns()
    qrt_bfr_rec_start = hdf.columns[hdf.columns.get_loc(rec_start) - 1]
    hdf['PriceRatio'] = hdf[qrt_bfr_rec_start].div(hdf[rec_bottom])
    subset_list = ul.to_records(index=False).tolist()
    ut = hdf.loc[hdf.index.isin(subset_list)]
    nut = hdf.loc[-hdf.index.isin(subset_list)]
    t,p = ttest_ind(ut['PriceRatio'],nut['PriceRatio'] , nan_policy='omit')
    different = True if p<0.01 else False
    better = "university town" if ut['PriceRatio'].mean() < nut['PriceRatio'].mean() else "non-university town"
    return(different, p, better)
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
get_list_of_university_towns()
get_recession_start()
get_recession_end()
get_recession_bottom()
convert_housing_data_to_quarters()
run_ttest()
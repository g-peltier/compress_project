import pandas as pd
import os
from tqdm import tqdm


def set_unique_index(df, date):
    """Return a dataframe with unique identifiers
    
    inputs:
        df (pd.DataFrame): a dataframe containing at least:
          - "nohhold": the index of the house
          - "nomem": the index of the person in the house
        year (int): the year of the dataframe.
    output:
        a dataframe with index:
            [YEAR][NOHHOLD][NOMEM]  (with NOHHOLD and NOMEM padded with 0
                                        on the left to have a 10 digit index)
    """
    # Check if df contains the necessary columns
    assert all([name in df.columns for name in ["nohhold", "nomem"]])

    # Pad the numbers to have a fixed length index
    nohhold = df.nohhold.astype(int)
    nohhold_norm = nohhold.astype(str).str.zfill(4)

    nomem = df.nomem.astype(int)
    nomem_norm = nomem.astype(str).str.zfill(4)

    return df.set_index((str(date) + nohhold_norm + nomem_norm).astype(int))


def get_df(list_data, year):
    """Create a complete dataframe from mutliple files
    
    inputs:
        list_data (list(pd.DataFrame)): list of dataframe such that combined
        the datasets contains all variables of interest.
        year (int): the year of the data
    output:
        a unique dataframe containing all variables from the different datasets. 
        Important : only the individual that appear in all dataset are kept in the
        return dataframe.
    """
       
    # Create a unique index for each dataframe
    list_data_norm = [set_unique_index(data, year) for data in list_data]

    # Get all indexes for each dataset (one index = one unique person)
    list_sets = [set(data_norm.index.values) for data_norm in list_data_norm]

    # Get the indexes that appear in all dataframes
    index_interest = list(list_sets[0].intersection(*list_sets[1:]))

    # Get the information on thoses appearing in all dataframes
    list_data_interest = [data.loc[index_interest] for data in list_data_norm]

    # Combine and merge dataset
    df = list_data_interest[0]
    for data in list_data_interest[1:]:
        df = df.combine_first(data)

    # adding bmi and year variables
    df = df.assign(year=year, bmi=df["gez2"] / (df["gez1"] * 0.01) ** 2)

    return df


# FONCTION TRÈS LONGUE !!!
def get_couples(df):
    """Return dataframe of every couples in the data
    
    input:
        df (pd.DataFrame): contains at least :
          - 'nohhold': the index of the house
          - 'positie': the 'rank' of the person in the house
    output:
        a list of tuple:
            (idx_1 (int), idx_2 (int), married (bool), year (int)) 
        of every couple that respond to the form and live in the same house.
    """
    
    # The rank denomination 
    part1_den = ("head of the household", 'head of')
    part2_den_spouse = ("spouse",)
    part2_den_perm = ("permanent partner (not married)", "permanen")

    list_couple = []
    groupby_house = df.groupby("nohhold")

    # For every house check if theire exist a part1_den and a part2_dem
    # if yes add to the list of couple there index and if they are married
    for name, group in groupby_house:

        try:
            den_house = group["positie"].str.lower()
        except:
            continue

        if den_house.isin(part1_den).sum() > 0:
            if den_house.isin(part2_den_spouse).sum() > 0:
                part1 = den_house[den_house.isin(part1_den)]
                part2 = den_house[den_house.isin(part2_den_spouse)]
                list_couple.append((part1.index.values[0], part2.index.values[0], 
                                    1, df['year'].unique()[0]))
            elif den_house.isin(part2_den_perm).sum() > 0:
                part1 = den_house[den_house.isin(part1_den)]
                part2 = den_house[den_house.isin(part2_den_perm)]
                list_couple.append((part1.index.values[0], part2.index.values[0],
                                    0, df['year'].unique()[0]))
            else:
                continue

    return pd.DataFrame(list_couple, columns=["part1", "part2", "married", "year"])


def get_all_data(path, column_interests, year_list=range(1993, 2003)):
    """Return a dataframe containing all info from year in year_list
    
    inputs: 
        path (str): the location of the data (.sav files)
        column_interests (list(str)): the name of the columns that we want
        each individual to have anwser to.
        year_list (list(int)): the years to fetch the data
    output:
        dataframe that contains all the information on individuals
    """
    
    list_df = []
    list_couple = []
    for year in tqdm(year_list):
        list_data = []

        # the hhi information was in inc for the year 1993
        if year > 1993:
            list_data.append(pd.read_spss(os.path.join(path, f'hhi{year}en.sav'))) 

        list_data.append(pd.read_spss(os.path.join(path, f'psy{year}en.sav')))
        list_data.append(pd.read_spss(os.path.join(path, f'inc{year}en.sav')))

        df = get_df(list_data, year)

        # small change if year 1994:
        if year == 1994:
            psy_columns = df.columns[df.columns.str.startswith('teg')]
            dict_psy = {old: new for (old, new) in zip(psy_columns, psy_columns.str[:-1])}
            df = df.rename(dict_psy, axis=1)
        # variable scholing changed name after 2001
        if year > 2001:
            df = df.rename({'oplzon': 'scholing'}, axis=1)
            
        df = df[column_interests].dropna()
        couple = get_couples(df)
        
        list_df.append(df)
        list_couple.append(couple)
        
    return pd.concat(list_df), pd.concat(list_couple)
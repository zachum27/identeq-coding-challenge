import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None) 
pd.set_option('display.max_rows', None)

def load_csv(file_name):
    return pd.read_csv(file_name)

def clense_data(dataframe):
    # Convert nulls to empty strings
    dataframe.fillna("", inplace=True)

    for col in dataframe.columns:
        dataframe[col] = dataframe[col].str.lower() # Standardise case (lower)
        dataframe[col] = dataframe[col].str.replace('[^\w\s]','') # Replace any character that isn't number / letter / whiespace with '' (empty)

def get_street_postcode_abp(abp_dataframe):
    # Iterates through abp df and populates dictionary with postcode and streetnames)
    search_dic = {} # Postcode : Streetnames (set)
    for index, row in abp_dataframe.iterrows():
        postcode = row['POSTCODE']
        street_name = row['STREET_NAME']
        if postcode in search_dic:
            search_dic[postcode].add(street_name)
        else:
            search_dic[postcode] = set([street_name])
    return search_dic # returns populated dictionary

def compare_address(input_dataframe, lookup):
    Street_In_Postcode = [] #Initialise list for yes / no result
    # Iterates through input_df and appends "Yes" to a list if postcode and streetname match, appends "No" if not
    for index, row in input_dataframe.iterrows(): 
        postcode = row['Postcode']
        match = 'No'
        if postcode in lookup: 
            line_1 = row['Address_Line_1']
            line_2 = row['Address_Line_2']
            line_3 = row['Address_Line_3']
            line_4 = row['Address_Line_4']
            for street in lookup[postcode]:
                if street in line_1 or street in line_2 or street in line_3 or street in line_4:
                    match = 'Yes'
        Street_In_Postcode.append(match)
    return Street_In_Postcode # Returns list of match results (yes / no)

def collate_data(input_csv_filename, street_in_postcode_list):
    # Add Street_In_Postcode results list to extra col in original input_dataframe
    dataframe = pd.read_csv(input_csv_filename)
    dataframe['Street_In_Postcode'] = street_in_postcode_list
    return dataframe

def export_to_csv(dataframe):    
    dataframe.to_csv('output.csv')

abp_df = load_csv('example_abp_data.csv')
input_df = load_csv('example_input_data.csv')
clense_data(input_df)
clense_data(abp_df)
postcode_street_dic = get_street_postcode_abp(abp_df)
result = compare_address(input_df, postcode_street_dic)
output_df = collate_data('example_input_data.csv', result)
export_to_csv(output_df)

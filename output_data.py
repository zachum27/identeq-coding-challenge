import pandas as pd

# Load csv into pandas dataframe
input_df = pd.read_csv('example_input_data.csv')
abp_df = pd.read_csv('example_abp_data.csv')

# Replace null values with empty string
input_df.fillna("", inplace=True)
abp_df.fillna("", inplace=True)

# print(input_df.info())
# print(abp_df.info())

# Initialise and populate dict {Postcode : Street_Name (set)}
check_dic = {}     
for index, row in abp_df.iterrows():
    postcode = row['POSTCODE']
    street_name = row['STREET_NAME']
    if postcode in check_dic:
        check_dic[postcode].add(street_name)
    else:
        check_dic[postcode] = set()

# Initialise and populate SIP list for result
Street_In_Postcode = []

for index, row in input_df.iterrows():
    postcode = str(row['Postcode'])
    match = 'No'
    if postcode in check_dic:
        line_1 = row['Address_Line_1']
        line_2 = row['Address_Line_2']
        line_3 = row['Address_Line_3']
        line_4 = row['Address_Line_4']
        
        for street in check_dic[postcode]:
            if street in line_1 or street in line_2 or street in line_3 or street in line_4:
                match = 'Yes'
    Street_In_Postcode.append(match)
    
# Add SIP results to extra col in df
input_df['Street_In_Postcode'] = Street_In_Postcode

print(input_df.info())
            
# Create output csv
input_df.to_csv('output.csv')
output = pd.read_csv('output.csv')
print(output.info())
    
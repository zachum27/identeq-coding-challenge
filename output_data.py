import pandas as pd

input_df = pd.read_csv('example_input_data.csv')
abp_df = pd.read_csv('example_abp_data.csv')

input_df.fillna("", inplace=True)
abp_df.fillna("", inplace=True)

print(input_df.info())
print(abp_df.info())

check_dic = {}     # Postcode : Street_Name

# Populate dict
for index, row in abp_df.iterrows():
    postcode = row['POSTCODE']
    street_name = row['STREET_NAME']
    if postcode in check_dic:
        check_dic[postcode].add(street_name)
    else:
        check_dic[postcode] = set()

# Initialise SIP list for result
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
        
input_df['Street_In_Postcode'] = Street_In_Postcode

print(input_df.info())
            
input_df.to_csv('output.csv')


output = pd.read_csv('output.csv')
print('info:')
print(output.info())
    
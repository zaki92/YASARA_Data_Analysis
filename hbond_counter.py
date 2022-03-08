# -*- coding: utf-8 -*-
"""
Reads raw YASARA simulation data for hbonds, and outputs the counts as a fraction
of time for all interfacial hydrogen bonds. Also provides mean energy and distance
for interfacial hbonds. Optional single column outputs also exist for further anal-
ysis if needed. 

Input : Excel file (.xlsx) output from YASARA (provided in GitHub as input data)
Output : Excel file(s) (.xlsx) with compiled interfacial hbond data (line 89)

Comment/Uncomment where indicated for optional outputs. 
Optional Outputs : All data single column (line 44)
                   All interfacial hbonds single column (line 58)
                   All distinct interfacial hbonds single column (line 69)
                   All distinct interfacial hbonds with only counts (line 78)
"""

import pandas as pd
import numpy as np
import time

start_time = time.time()

#input the yasara analysis file (saved as an excel file) here
df = pd.read_excel('input_data_S477N_all_hbonds_v2.xlsx')

#starting and ending indices for hbond data, retrieved automatically here
start_location = np.where(df.columns.str.contains('SlvH'))[0][0] + 1
end_location = np.where(df.columns.str.contains('Gyra'))[0][0]
number_of_snapshots =  len(df.iloc[:-3, 1])

#saving the hbond info in a different dataframe
df_hbond = df.iloc[:-3,start_location:end_location]
column_length = len(df_hbond.iloc[0,:])

#collapsing everything in a single column
if column_length > 4:
    df_single_column = df_hbond.iloc[:,0:4] 
    for i in range(4,column_length,4):
        df_temp = df_hbond.iloc[:,i:i+4]
        df_temp.columns = df_single_column.columns
        df_single_column = pd.concat((df_single_column,df_temp)
                                     ,axis = 0)
else: 
    df_single_column = df_hbond

#uncomment the next line to get all bonds as well as null values as an excel file
df_single_column.to_excel('single_column_all_data_int1.xlsx')

#eliminating rows with '-' as entries to get all hbonds listed
filter_data_1 = (df_single_column.iloc[:,0].str.contains('-')) ^ (df_single_column.iloc[:,0])
df_single_valid = df_single_column[filter_data_1]

#filtering the data to get interfacial bonds only
filter_data_2 = ((df_single_valid.iloc[:,0].str.split(".").str[2]) != 
                (df_single_valid.iloc[:,1].str.split(".").str[2]))

df_single_all_interfacial = df_single_valid[filter_data_2]

#uncomment the next line to get all interfacial bonds specifically as an excel file
df_single_all_interfacial.to_excel('all_interfacial_bonds_int2.xlsx')

#the next section will clean the columns to only output residue number
df_single_residue_interfacial = df_single_all_interfacial
df_single_residue_interfacial.iloc[:,0] = (df_single_residue_interfacial.iloc[:,0].str.split(".").str[1] 
                                          + "." + df_single_residue_interfacial.iloc[:,0].str.split(".").str[2])
df_single_residue_interfacial.iloc[:,1] = (df_single_residue_interfacial.iloc[:,1].str.split(".").str[1] 
                                           + "." + df_single_residue_interfacial.iloc[:,1].str.split(".").str[2])

#uncomment the next line to get all interfacial bonds specifically as an excel file
df_single_residue_interfacial.to_excel('all_residue_interfacial_bonds_int3.xlsx')

grp_1 = df_single_residue_interfacial.columns[0]
grp_2 = df_single_residue_interfacial.columns[1]

#outputs all hbond ratios to a single excel file 
df_counts = df_single_residue_interfacial.groupby([grp_1, grp_2]).size().to_frame('counts/snapshot')
df_counts = df_counts/number_of_snapshots 

#uncomment the next line if you want just the counts to excel
#df_counts.to_excel('hbond_counts_as_fraction_of_time.xlsx')

df_energy_distance = df_single_residue_interfacial.groupby([grp_1, grp_2]).sum()

#merging the energy distance data with the counts
df_final = pd.concat((df_energy_distance,df_counts), axis = 1)
df_final.iloc[:,0] = df_final.iloc[:,0] / (df_final.iloc[:,2]*number_of_snapshots)
df_final.iloc[:,1] = df_final.iloc[:,1] / (df_final.iloc[:,2]*number_of_snapshots)
columns_new = ['mean_energy (kJ/mol)','mean_distance (A)','counts/snapshot']
df_final.columns = columns_new

#saving the final output to an excel file
df_final.to_excel('final_cleaned_output_compiled_hbond_energy_distance.xlsx')

print('Time:',time.time()-start_time)









import pandas as pd
import scipy
from scipy.stats import gmean
import matplotlib.pyplot as plt

plt.close("all")
 


#The purpose of this program is to identify the top 20 exporters in the
#provided data set (import_export_dataset.csv)
#Plot all of them on one graph

#So far this program shows the process I took to
#1. read data
#2. parse out two countries
#3. combine the two countries onto one dataframe
#4. plot

#This is a global way to format my style for select amount of decimals
pd.options.display.float_format = '{:,.0f}'.format

#####################
### 1. Read file ####
#####################

import_export = pd.read_csv("import_export_dataset.csv")




##################################
### 2. Parse out Two Countries ###
##################################


#Change DataFrame to show only Year and Export for columns
"""Columns of interest: 'Year', 'Export (US$ Thousand)', 'Import (US$ Thousand)'"""


import_export_year_export = import_export.loc[:, ['Partner Name', 'Year', 'Export (US$ Thousand)']]


#After describing, the values have too many digits.
#Can I change the values to have no decimal places? Format specifier?
#Try to format a single column now to 0.1f
"""
Possible answer: 
format_dict = {
    'Export (US$ Thousand)': '{:.1%}'
}

"""

# our dataframe containing the data is called contribution
# Below are some notes on how to specify format
"""
source: https://kiwidamien.github.io/stylish-pandas.html
# set ALL float columns to '${:,.2f}' formatting (including the percentage)
format_dict = {col_name: '${:,.2f}' for col_name in contribution.select_dtypes(float).columns}
# override the percentage column
format_dict['Individual % of total'] = '{:.1%}'
contribution.head().style.format(format_dict)
#'{:,.2f}'.format
"""
"""
format_dict = {col_name: '${:,.2f}' for col_name in import_export_year_export.select_dtypes(float).columns}
import_export_year_export.style.format(format_dict)
s = import_export_year_export.style.format('{:.0f}')
print(s)
"""

#ERROR USING STYLER: <pandas.io.formats.style.Styler object at 0x0000021075021AB0>
"""
df = import_export_year_export.style \
  .format(precision=3, thousands=".", decimal=",") \
  .format_index(str.upper, axis=1)

print(df)
"""

#Anyways
#Calculate Harmonic Mean of Each Country. Should store it somewhere
#New column for Harmonic Mean

#Create new column called 'Harmonic Mean'
#Use df.insert(1, "newcol", [99, 99])
"""
something = stats.hmean(import_export_year_export.loc[:,"Export (US$ Thousand)"])
print("\n---------\n")
print("something: ",  something)
"""
#s = scipy.stats.gmean(import_export_year_export.loc[:,'Export (US$ Thousand)'])
#print(s)

#try to print single value
singleValue = import_export_year_export.loc[:,'Export (US$ Thousand)'][5]


#Try to print out unique values of countries
#Amount of unique values: value_counts()
value_counts = import_export_year_export.iloc[:,1].value_counts()
print("\n\nvalue counts: %d\n\n", value_counts)

unique = import_export_year_export.iloc[:,0].unique()
print("\n\nunique places: ", unique)


#reindex
#import_export_year_export = import_export_year_export.reset_index(drop=True)
print("import_export_year_export: ", import_export_year_export.head())



#find mean for Aruba
aruba = import_export_year_export.loc[import_export_year_export['Partner Name'] == 'Aruba']

aruba_export_values = aruba.loc[:,'Export (US$ Thousand)']

aruba_mean = scipy.stats.hmean(aruba_export_values.iloc[-1])
print("aruba mean: ", aruba_mean)

#Plot aruba Export vs Year Line Plot
aruba_export_vs_year = import_export_year_export.loc[import_export_year_export['Partner Name'] == 'Aruba', ['Year', 'Export (US$ Thousand)']]


### REINDEXING ###

#aruba_export_vs_year = aruba_export_vs_year.reset_index(drop=True)
aruba_export_vs_year = aruba_export_vs_year.set_index('Year')
print("\n\tARUBA\n", aruba_export_vs_year)


#Plot next country Export vs Year 
next_country = unique[1]
print("next country: ", next_country)

#Plot next_country (Afghanistan) to the same plot
#Export vs Year
afghanistan_export_vs_year = import_export_year_export.loc[import_export_year_export['Partner Name'] == 'Afghanistan', ['Year', 'Export (US$ Thousand)']]
afghanistan_export_vs_year = afghanistan_export_vs_year.set_index('Year')
print("afghanistan: ", type(afghanistan_export_vs_year))

##############################
### COMBINE TWO DATAFRAMES ###
##############################


print("\n\tAfghanistan\n ", afghanistan_export_vs_year)

combined_dataFrame = pd.merge(aruba_export_vs_year, afghanistan_export_vs_year, on='Year')
print(combined_dataFrame)

#Rename Column
combined_dataFrame.rename(columns = {'Export (US$ Thousand)_x':'Aruba', 'Export (US$ Thousand)_y': 'Afghanistan'}, inplace = True)
print(combined_dataFrame)



#################
###### PLOT #####
#################

plt.figure();
combined_dataFrame.plot()
plt.show()

#Here we took a large data set and compared a specific variable over time of two countries

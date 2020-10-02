import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

prec_file = json.load(open("US_Precipitation.json",))    #Load Precipitation dataset
df_crime = pd.read_csv("Intentional_Homicides and_Other_Crimes.csv",encoding = "ISO-8859-1")  #Load homicide dataset

#Format precipitation dataset
df_prec = pd.DataFrame.from_dict(prec_file['data']).T   
df_prec = df_prec.astype(float)

#Format homicide dataset
df_crime.columns = ['T12','Country','Year','Intentional_Homicide','Y','Z','A']
df_hom = df_crime[df_crime.Intentional_Homicide == 'Intentional homicide rates per 100,000']

#Select countries of interest for the homicide plot
countries = ['United States of America','Australia','United Kingdom',
             'United Arab Emirates','Algeria']
df_hom = df_hom[df_hom.Year == '2010']
df_hom = df_hom[df_hom.Country.isin(countries)]
df_hom.drop(['T12','Z','A'],axis = 1,inplace = True)
df_hom.Y = df_hom.Y.astype('float')

#Plot a bar graph of the 5 selected countries for homicide data
f1 = plt.figure(1)
plt.bar(df_hom.Country,df_hom.Y)
plt.xticks(rotation = 90)
plt.title('Homicide Rates in 5 different countries in 2010')
plt.ylabel('Intentional homicide rates per 100,000')
plt.tight_layout()

#Get a best fit line for the precipitation dataset
x = np.array(df_prec.index.astype(float))
y = np.array(df_prec.value)
m, b = np.polyfit(x, y, 1)
best_fit = []
for i in df_prec.index.astype(float):
    best_fit.append(m*i+b)
index = list(df_prec.index)
for i in range(len(index)):
    index[i] = index[i][0:4]
df_prec['bestfit'] = best_fit

#Reindex the precipitation dataset to the actual years
df_prec['index'] = index
df_prec = df_prec.set_index(['index'])

#Plot the precipitation and its best fit line
f2 = plt.figure(2)
df_prec.value.plot()
df_prec.bestfit.plot()
plt.title('Precipitation inches in the USA from years 1895 to 2015')
plt.ylabel('Inches of Precipitation')
plt.xlabel('Year')
plt.legend(['Precipitation over time','Best fit line to show increase']) 
plt.show()

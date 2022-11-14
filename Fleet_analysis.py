# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 16:26:20 2022

@author: janva
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
path = r'C:\Users\janva\Emobpy\example\db\Fleets/'

#Import files 
#Situation 1 - Uncontrolled
Fleet_uncontrolled = pd.read_csv(path+'Fleet1_uncontrolled.csv').set_index('date')
Fleet_uncontrolled_home = pd.read_csv(path +'Fleet1_uncontrolled_home.csv').set_index('date')
Fleet1_state = pd.read_csv(path +'Fleet1_uncontrolled_state.csv').set_index('date')
Fleet_uncontrolled2 = pd.read_csv(path+'Fleet1_uncontrolled2.csv').set_index('date')
Fleet_uncontrolled2_home = pd.read_csv(path +'Fleet1_uncontrolled2_home.csv').set_index('date')


#Situation 2 - Night Charge 
Fleet_nightcharge = pd.read_csv(path+'Fleet1_nightcharge.csv').set_index('date')
Fleet_nightcharge_home = pd.read_csv(path +'Fleet1_nightcharge_home.csv').set_index('date')
Fleet_nightcharge2 = pd.read_csv(path+'Fleet1_nightcharge2.csv').set_index('date')
Fleet_nightcharge2_home = pd.read_csv(path +'Fleet1_nightcharge2_home.csv').set_index('date')


#Situation 3 - Combined charging strategies 
Fleet_combined = pd.read_csv(path+'Fleet1_combinedstrategies.csv').set_index('date')
Fleet_combined_home = pd.read_csv(path +'Fleet1_combinedstrategies_home.csv').set_index('date')
Fleet_combined2 = pd.read_csv(path+'Fleet1_combinedstrategies2.csv').set_index('date')
Fleet_combined2_home = pd.read_csv(path +'Fleet1_combinedstrategies2_home.csv').set_index('date')

#Situation 4 - Smaller cars 
Fleet_smaller = pd.read_csv(path+'Fleet4_smallercars.csv').set_index('date')
Fleet_smaller_home = pd.read_csv(path +'Fleet4_smallercars_home.csv').set_index('date')
Fleet4_state = pd.read_csv(path +'Fleet4_smallercars_state.csv').set_index('date')
Fleet_smaller2 = pd.read_csv(path+'Fleet4_smallercars2.csv').set_index('date')
Fleet_smaller2_home = pd.read_csv(path +'Fleet4_smallercars2_home.csv').set_index('date')
Fleet4_state2 = pd.read_csv(path +'Fleet4_smallercars2_state.csv').set_index('date')

#Situation 5 - Less charger probability and 0.4 at work (instead of 1.0)
Fleet_chargerprob = pd.read_csv(path+'Fleet5_chargerprob.csv').set_index('date')
Fleet_chargerprob_home = pd.read_csv(path +'Fleet5_chargerprob_home.csv').set_index('date')
Fleet5_state = pd.read_csv(path +'Fleet5_chargerprob_state.csv').set_index('date')
#Situation 5.2 - Less charger probability and 0.0 at work (instead of 1.0)
Fleet_chargerprob2 = pd.read_csv(path+'Fleet5_chargerprob2.csv').set_index('date')
Fleet_chargerprob2_home = pd.read_csv(path +'Fleet5_chargerprob2_home.csv').set_index('date')
Fleet5_state2 = pd.read_csv(path +'Fleet5_chargerprob2_state.csv').set_index('date')

#Combine different fleets and/or locations 
data = [Fleet_uncontrolled['0'], Fleet_uncontrolled_home['0'], Fleet_uncontrolled2['0'], Fleet_uncontrolled2_home['0'], Fleet_nightcharge['0'], Fleet_nightcharge_home['0'], Fleet_nightcharge2['0'], Fleet_nightcharge2_home['0'], Fleet_combined['0'], Fleet_combined_home['0'], Fleet_combined2['0'], Fleet_combined2_home['0'], Fleet_smaller['0'], Fleet_smaller_home['0'], Fleet_smaller2['0'], Fleet_smaller2_home['0'], Fleet_chargerprob['0'], Fleet_chargerprob_home['0'], Fleet_chargerprob2['0'], Fleet_chargerprob2_home['0']]
headers = ['Uncontrolled','Uncontrolled_home', 'Uncontrolled2','Uncontrolled2_home', 'Nightcharge','Nightcharge_home', 'Nightcharge2','Nightcharge2_home','Combined','Combined_home','Combined2','Combined2_home','Smaller','Smaller_home','Smaller2','Smaller2_home','Chargerprob','Chargerprob_home','Chargerprob2','Chargerprob2_home']
Fleet = pd.concat(data,axis=1,keys=headers)

#Set datetime index 
Fleet.index = pd.to_datetime(Fleet.index)

#MWh to kWh
Fleet = Fleet*1000

#Remove outliers
Fleet[Fleet > 500] = 0

#Hourly average
Houravg_Fleet = Fleet.groupby(Fleet.index.hour).mean()

#Weekly average
Weekavg_Fleet = Fleet.groupby(Fleet.index.dayofweek).mean()

#Sum
Total_Fleet_kWh = Fleet.sum()


#%% Seasons
data_winter = [Fleet[pd.Timestamp('2016-12-01'): pd.Timestamp('2016-12-31')],Fleet[pd.Timestamp('2016-01-01'): pd.Timestamp('2016-03-01')]]
Winter = pd.concat(data_winter)
Spring = Fleet[pd.Timestamp('2016-03-01'): pd.Timestamp('2016-06-01')]
Summer = Fleet[pd.Timestamp('2016-06-01'): pd.Timestamp('2016-09-01')]
Autumn = Fleet[pd.Timestamp('2016-09-01'): pd.Timestamp('2016-12-01')]

# Houravg_Winter = Winter.groupby(Winter.index.hour).mean()
# Houravg_Spring = Spring.groupby(Spring.index.hour).mean()
# Houravg_Summer = Summer.groupby(Summer.index.hour).mean()
# Houravg_Autumn = Autumn.groupby(Autumn.index.hour).mean()

#%% Home location 
Home_Fleet = Fleet1_state.replace(['home'],1)
Home_Fleet = Home_Fleet.replace(['errands','escort','leisure','shopping','workplace','driving'],0)
Total_Home_Fleet = Home_Fleet.sum(axis=1)/len(Home_Fleet.columns)*100
Total_Home_Fleet.index = pd.to_datetime(Total_Home_Fleet.index)
Total_Home_Fleet = Total_Home_Fleet.resample('h').mean()                         #Minimum availability 
Total_Home_Fleet_avg = Total_Home_Fleet.mean()

#%% Driving 
Driving_Fleet = Fleet1_state.replace(['driving'],1)
Driving_Fleet = Driving_Fleet.replace(['errands','escort','leisure','shopping','workplace','home'],0)
Total_Driving_Fleet = Driving_Fleet.sum(axis=1)/len(Home_Fleet.columns)*100
Total_Driving_Fleet.index = pd.to_datetime(Total_Driving_Fleet.index)
Total_Driving_Fleet = Total_Driving_Fleet.resample('h').mean()                   #Maximum cars driving
Total_Driving_Fleet_avg = Total_Driving_Fleet.mean()

# #%% Plots 
#Car availability 
#Minimum cars at home 
plt.figure()
plt.figure(figsize=(15,8))
plt.plot(Total_Home_Fleet)
plt.axhline(y=Total_Home_Fleet_avg, color = 'r', linestyle = '--',linewidth=4)
plt.title('Car availability')
plt.xlabel('Time')
plt.xlim(pd.Timestamp('2016-01-01'), pd.Timestamp('2016-01-07'))
plt.ylabel('Percentage cars at home')
plt.legend(['Cars at home','Average'])
plt.show()

#Driving cars 
plt.figure()
plt.figure(figsize=(15,8))
plt.plot(Total_Driving_Fleet)
plt.axhline(y=Total_Driving_Fleet_avg, color = 'r', linestyle = '--',linewidth=4)
plt.title('Cars driving')
plt.xlim(pd.Timestamp('2016-01-01'), pd.Timestamp('2016-01-07'))
plt.xlabel('Time')
plt.ylabel('Percentage of cars driving')
plt.legend(['Cars driving','Average'])
plt.show()

#Yearly charging demand 
#Smaller cars 
plt.figure()
plt.figure(figsize=(15,8))
plt.plot(Fleet['Smaller'],linewidth=1)
plt.title('Yearly charging demand - Smaller cars')
plt.xlabel('Time')
plt.ylabel('Charging demand [kWh]')
plt.show()

plt.figure()
plt.figure(figsize=(15,8))
plt.plot(Fleet['Smaller_home'],linewidth=1)
plt.title('Yearly charging demand at home - Smaller cars')
plt.xlabel('Time')
plt.ylabel('Charging demand [kWh]')
plt.show()


#Hourly average - Uncontrolled
plt.figure()
plt.plot(Houravg_Fleet['Uncontrolled'])
plt.plot(Houravg_Fleet['Uncontrolled_home'])
plt.title('Hourly Average Fleet - Uncontrolled')
plt.legend(['Total fleet','Fleet at home'])
plt.ylim([0,90])
plt.xlim([0,23])
plt.xlabel('Time [Hours]')
plt.ylabel('Charging demand [kWh]')
plt.show()

#Weekly average - Uncontrolled
plt.figure()
plt.plot(Weekavg_Fleet['Uncontrolled'])
plt.plot(Weekavg_Fleet['Uncontrolled_home'])
plt.title('Average day of week Fleet - Uncontrolled')
plt.legend(['Total fleet','Fleet at home'])
plt.ylim([0,62])
plt.xlim([0,6])
plt.xlabel('Time [Hours]')
plt.ylabel('Charging demand [kWh]')
plt.show()

#Hourly average - Night Charge 
plt.figure()
plt.plot(Houravg_Fleet['Nightcharge'])
plt.plot(Houravg_Fleet['Nightcharge_home'])
plt.title('Hourly Average Fleet - Night charge')
plt.legend(['Total fleet','Fleet at home'])
plt.ylim([0,90])
plt.xlim([0,23])
plt.xlabel('Time [Hours]')
plt.ylabel('Charging demand [kWh]')
plt.show()

#Weekly average - Night Charge 
plt.figure()
plt.plot(Weekavg_Fleet['Nightcharge'])
plt.plot(Weekavg_Fleet['Nightcharge_home'])
plt.title('Average day of week Fleet - Night Charge')
plt.legend(['Total fleet','Fleet at home'])
plt.xlabel('Time [Hours]')
plt.ylabel('Charging demand [kWh]')
plt.show()

#Hourly average - Combined strategies 
plt.figure()
plt.plot(Houravg_Fleet['Combined'])
plt.plot(Houravg_Fleet['Combined_home'])
plt.title('Hourly Average Fleet - Combined strategies')
plt.legend(['Total fleet','Fleet at home'])
plt.xlabel('Time [Hours]')
plt.ylabel('Charging demand [kWh]')
plt.show()

#Weekly average - Combined strategies 
plt.figure()
plt.plot(Weekavg_Fleet['Combined'])
plt.plot(Weekavg_Fleet['Combined_home'])
plt.title('Day of week Average Average Fleet - Combined strategies')
plt.legend(['Total fleet','Fleet at home'])
plt.xlabel('Time [Hours]')
plt.ylabel('Charging demand [kWh]')
plt.show()

#Hourly average - Smaller cars 
plt.figure()
plt.plot(Houravg_Fleet['Smaller'])
plt.plot(Houravg_Fleet['Smaller_home'])
plt.title('Hourly Average Fleet - Smaller cars')
plt.legend(['Total fleet','Fleet at home'])
plt.xlabel('Time [Hours]')
plt.ylabel('Charging demand [kWh]')
plt.show()

#Weekly average - Smaller cars  
plt.figure()
plt.plot(Weekavg_Fleet['Smaller'])
plt.plot(Weekavg_Fleet['Smaller_home'])
plt.title('Day of week Average Average Fleet - Smaller cars')
plt.legend(['Total fleet','Fleet at home'])
plt.xlabel('Time [Hours]')
plt.ylabel('Charging demand [kWh]')
plt.show()


## Comparisson situations 
#Hourly average
plt.figure()
plt.figure(figsize=(8,5))
plt.plot(Houravg_Fleet['Uncontrolled'])
plt.plot(Houravg_Fleet['Nightcharge'])
plt.plot(Houravg_Fleet['Combined'])
plt.plot(Houravg_Fleet['Combined2'])
plt.plot(Houravg_Fleet['Smaller'])
plt.plot(Houravg_Fleet['Smaller2'])
plt.plot(Houravg_Fleet['Chargerprob'])
plt.title('Hourly Average Fleet - Anywhere')
plt.legend(['Uncontrolled','Night Charge','Combined','Combined2','Smaller cars','Smaller cars 2','Lower charger probability'])
plt.xlabel('Time [Hours]')
plt.ylabel('Charging demand [kWh]')
plt.show()

#Weekly average
plt.figure()
plt.figure(figsize=(8,5))
plt.plot(Weekavg_Fleet['Uncontrolled'])
plt.plot(Weekavg_Fleet['Nightcharge'])
plt.plot(Weekavg_Fleet['Combined'])
plt.plot(Weekavg_Fleet['Combined2'])
plt.plot(Weekavg_Fleet['Smaller'])
plt.plot(Weekavg_Fleet['Smaller2'])
plt.plot(Weekavg_Fleet['Chargerprob'])
plt.title('Daily Average per week Fleet - Anywhere')
plt.legend(['Uncontrolled','Night Charge','Combined','Combined2','Smaller cars','Smaller cars 2','Lower charger probability'])
plt.xlabel('Time [Hours]')
plt.ylabel('Charging demand [kWh]')
plt.show()


## Comparisson situations 
#Hourly average
plt.figure()
x = np.arange(0,24)
plt.figure(figsize=(10,6))
plt.plot(Houravg_Fleet['Uncontrolled'],color='green',label='Uncontrolled')
plt.plot(Houravg_Fleet['Uncontrolled2'],color='green')
plt.fill_between(x,Houravg_Fleet['Uncontrolled'], Houravg_Fleet['Uncontrolled2'],facecolor='green',alpha=0.4)
plt.plot(Houravg_Fleet['Nightcharge'],color='yellow',label='Night Charge')
plt.plot(Houravg_Fleet['Nightcharge2'],color='yellow')
plt.fill_between(x,Houravg_Fleet['Nightcharge'], Houravg_Fleet['Nightcharge2'],facecolor='yellow',alpha=0.4)
plt.plot(Houravg_Fleet['Combined'],color='blue',label='Combined')
plt.plot(Houravg_Fleet['Combined2'],color='blue')
plt.fill_between(x,Houravg_Fleet['Combined'], Houravg_Fleet['Combined2'],facecolor='blue',alpha=0.4)
plt.plot(Houravg_Fleet['Smaller'],color='red',label='Combined - Smaller cars')
plt.plot(Houravg_Fleet['Smaller2'],color='red')
plt.fill_between(x,Houravg_Fleet['Smaller'], Houravg_Fleet['Smaller2'],facecolor='red',alpha=0.4)
plt.title('Hourly Average - Total fleet')
plt.legend()
plt.ylim([0,90])
plt.xlim([0,23])
plt.xlabel('Time [Hours]')
plt.ylabel('Charging demand [kWh]')
plt.show()

#Hourly average - Home
plt.figure()
x = np.arange(0,24)
plt.figure(figsize=(10,6))
plt.plot(Houravg_Fleet['Uncontrolled_home'],color='green',label='Uncontrolled')
plt.plot(Houravg_Fleet['Uncontrolled2_home'],color='green')
plt.fill_between(x,Houravg_Fleet['Uncontrolled_home'], Houravg_Fleet['Uncontrolled2_home'],facecolor='green',alpha=0.4)
plt.plot(Houravg_Fleet['Nightcharge_home'],color='yellow',label='Night Charge_home')
plt.plot(Houravg_Fleet['Nightcharge2_home'],color='yellow')
plt.fill_between(x,Houravg_Fleet['Nightcharge_home'], Houravg_Fleet['Nightcharge2_home'],facecolor='yellow',alpha=0.4)
plt.plot(Houravg_Fleet['Combined_home'],color='blue',label='Combined')
plt.plot(Houravg_Fleet['Combined2_home'],color='blue')
plt.fill_between(x,Houravg_Fleet['Combined_home'], Houravg_Fleet['Combined2_home'],facecolor='blue',alpha=0.4)
plt.plot(Houravg_Fleet['Smaller_home'],color='red',label='Combined - Smaller cars')
plt.plot(Houravg_Fleet['Smaller2_home'],color='red')
plt.fill_between(x,Houravg_Fleet['Smaller_home'], Houravg_Fleet['Smaller2_home'],facecolor='red',alpha=0.4)
plt.title('Hourly Average - Fleet at home')
plt.legend()
plt.ylim([0,90])
plt.xlim([0,23])
plt.xlabel('Time [Hours]')
plt.ylabel('Charging demand [kWh]')
plt.show()

#Weekly average
plt.figure()
x = np.arange(0,7)
plt.figure(figsize=(10,6))
plt.plot(Weekavg_Fleet['Uncontrolled'],color='green',label='Uncontrolled')
plt.plot(Weekavg_Fleet['Uncontrolled2'],color='green')
plt.fill_between(x,Weekavg_Fleet['Uncontrolled'], Weekavg_Fleet['Uncontrolled2'],facecolor='green',alpha=0.4)
plt.plot(Weekavg_Fleet['Nightcharge'],color='yellow',label='Night Charge')
plt.plot(Weekavg_Fleet['Nightcharge2'],color='yellow')
plt.fill_between(x,Weekavg_Fleet['Nightcharge'], Weekavg_Fleet['Nightcharge2'],facecolor='yellow',alpha=0.4)
plt.plot(Weekavg_Fleet['Combined'],color='blue',label='Combined')
plt.plot(Weekavg_Fleet['Combined2'],color='blue')
plt.fill_between(x,Weekavg_Fleet['Combined'], Weekavg_Fleet['Combined2'],facecolor='blue',alpha=0.4)
plt.plot(Weekavg_Fleet['Smaller'],color='red',label='Combined - Smaller cars')
plt.plot(Weekavg_Fleet['Smaller2'],color='red')
plt.fill_between(x,Weekavg_Fleet['Smaller'], Weekavg_Fleet['Smaller2'],facecolor='red',alpha=0.4)
plt.title('Average day of week - Total fleet')
plt.legend()
plt.xlim([0,6])
# plt.ylim([0,60])
plt.xlabel('Time [Days]')
plt.ylabel('Charging demand [kWh]')
plt.show()

#Weekly average - Home
plt.figure()
x = np.arange(0,7)
plt.figure(figsize=(10,6))
plt.plot(Weekavg_Fleet['Uncontrolled_home'],color='green',label='Uncontrolled')
plt.plot(Weekavg_Fleet['Uncontrolled2_home'],color='green')
plt.fill_between(x,Weekavg_Fleet['Uncontrolled_home'], Weekavg_Fleet['Uncontrolled2_home'],facecolor='green',alpha=0.4)
plt.plot(Weekavg_Fleet['Nightcharge_home'],color='yellow',label='Night Charge_home')
plt.plot(Weekavg_Fleet['Nightcharge2_home'],color='yellow')
plt.fill_between(x,Weekavg_Fleet['Nightcharge_home'], Weekavg_Fleet['Nightcharge2_home'],facecolor='yellow',alpha=0.4)
plt.plot(Weekavg_Fleet['Combined_home'],color='blue',label='Combined')
plt.plot(Weekavg_Fleet['Combined2_home'],color='blue')
plt.fill_between(x,Weekavg_Fleet['Combined_home'], Weekavg_Fleet['Combined2_home'],facecolor='blue',alpha=0.4)
plt.plot(Weekavg_Fleet['Smaller_home'],color='red',label='Combined - Smaller cars')
plt.plot(Weekavg_Fleet['Smaller2_home'],color='red')
plt.fill_between(x,Weekavg_Fleet['Smaller_home'], Weekavg_Fleet['Smaller2_home'],facecolor='red',alpha=0.4)
plt.title('Average day of week - Fleet at home')
plt.legend()
plt.xlim([0,6])
# plt.ylim([0,60])
plt.xlabel('Time [Days]')
plt.ylabel('Charging demand [kWh]')
plt.show()



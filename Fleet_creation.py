# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 11:16:58 2022

@author: janva
"""
"""
TS = Tesla model S
T3 = Tesla model 3
RZ = Renault Zoe
HK = Hyundai Kona

I = inactive
W = Working
"""
import os
import pandas as pd


#%% Path can be changed for different databases per situation 
path = r'C:\Users\janva\Emobpy\example\db\situation1234'
path2 = r'C:\Users\janva\Emobpy\example\db_jup'
#Give different output name according to situation
Output_name = 'Fleet1_balanced'                                            

#%% Number of generated input files that you want to load in, these files are 
#   used for the fleet generation below 
TS_inactive = 10
TS_working = 30

T3_inactive = 17
T3_working = 53

RZ_inactive = 8
RZ_working = 22

HK_inactive = 15
HK_working = 45


#%%Create a fleet by chosing different cars and charging strategies.
#  Don't exceed the number of generated input files per car and activity 
#Tesla model S - Inactive
EV_TSI_balanced = 10
EV_TSI_uncontrolled = 0
EV_TSI_nightcharge = 0

#Tesla model S - Working
EV_TSW_balanced = 30
EV_TSW_uncontrolled = 0
EV_TSW_nightcharge = 0

#Tesla model 3 - Inactive
EV_T3I_balanced = 17
EV_T3I_uncontrolled = 0
EV_T3I_nightcharge = 0

#Tesla model 3 - Working
EV_T3W_balanced = 53
EV_T3W_uncontrolled = 0
EV_T3W_nightcharge = 0

#Renault Zoe - Inactive
EV_RZI_balanced = 8
EV_RZI_uncontrolled =0
EV_RZI_nightcharge = 0

#Renault Zoe - Working
EV_RZW_balanced = 22
EV_RZW_uncontrolled = 0
EV_RZW_nightcharge = 0

#Hyundai Kona - Inactive
EV_HKI_balanced = 15
EV_HKI_uncontrolled = 0
EV_HKI_nightcharge = 0

#Hyundai Kona - Working
EV_HKW_balanced = 45
EV_HKW_uncontrolled = 0
EV_HKW_nightcharge = 0


#%% All files loaded in and combined using loops 
#Tesla model S - Inactive 
Data_TSI = list()
Charge_TSI = list()
TSI = list()
TSI_home = list()
# Fleet = list()
TSI_balanced = pd.DataFrame()
TSI_uncontrolled = pd.DataFrame()
TSI_nightcharge = pd.DataFrame()
TSI_home_balanced = pd.DataFrame()
TSI_home_uncontrolled = pd.DataFrame()
TSI_home_nightcharge = pd.DataFrame()
TSI_state = pd.DataFrame()

for i in range (1,TS_inactive+1):
    file_path_TSI = os.path.join(path,'TS','inactive'+str(i))
    Temp_data_TSI = pd.read_csv(os.path.join(file_path_TSI,"All_data.csv"))
    Temp_data_TSI['date'] = pd.DataFrame({'Hours': pd.date_range('2016-01-01', '2016-12-31', freq='15min')})
    Temp_data_TSI.set_index('date',inplace=True)
    Data_TSI.append(Temp_data_TSI)
    for l in range (0,len(TSI)):
        TSI_state.loc[:,'TSI'+str(l)] = TSI[l]['state']
    Temp_charge_TSI = pd.read_csv(os.path.join(file_path_TSI,"bev_time_series.csv"),header=([0]),skiprows=[1,2,3])
    Temp_charge_TSI['date'] =  pd.DataFrame({'Hours': pd.date_range('2016-01-01', '2016-12-31', freq='1H')})
    Temp_charge_TSI = Temp_charge_TSI[['date', 'balanced_MWh', 'immediate_MWh', 'from_23_to_8_at_any_MWh', 'from_0_to_24_at_home_MWh']]
    Temp_charge_TSI.set_index('date',inplace=True)
    Temp_charge_TSI = Temp_charge_TSI.resample('15min').ffill()
    Charge_TSI.append(Temp_charge_TSI)
    Temp_TSI = pd.concat([Temp_data_TSI,Temp_charge_TSI],axis=1)
    TSI.append(Temp_TSI)
    Temp_TSI_home = Temp_TSI[Temp_TSI['state'].str.contains('home')]
    Temp_TSI_home = Temp_TSI_home.fillna(0)
    TSI_home.append(Temp_TSI_home)
    # for j in range (len(TSI)):  
    #     globals()[f"TSI{j}"] = TSI[j]
    #     TSI[j].to_csv(os.path.join(path2,'TSI'+str(j)+'.csv'))
    for k in range (len(TSI)):
        TSI_balanced.loc[:,'TSIB'+str(k)] = TSI[k]['balanced_MWh']
        TSI_uncontrolled.loc[:,'TSIU'+str(k)] = TSI[k]['immediate_MWh']
        TSI_nightcharge.loc[:,'TSINC'+str(k)] = TSI[k]['from_23_to_8_at_any_MWh']
        TSI_home_balanced.loc[:,'TSIB'+str(k)] = TSI_home[k]['balanced_MWh']
        TSI_home_uncontrolled.loc[:,'TSIU'+str(k)] = TSI_home[k]['immediate_MWh']
        TSI_home_nightcharge.loc[:,'TSINC'+str(k)] = TSI_home[k]['from_23_to_8_at_any_MWh']

#%% Tesla model S - Working
Data_TSW = list()
Charge_TSW = list()
TSW = list()
TSW_home = list()
TSW_balanced = pd.DataFrame()
TSW_uncontrolled = pd.DataFrame()
TSW_nightcharge = pd.DataFrame()
TSW_home_balanced = pd.DataFrame()
TSW_home_uncontrolled = pd.DataFrame()
TSW_home_nightcharge = pd.DataFrame()
TSW_state = pd.DataFrame()

for i in range (1,TS_working+1):
    file_path_TSW = os.path.join(path,'TS','working'+str(i))
    Temp_data_TSW = pd.read_csv(os.path.join(file_path_TSW,"All_data.csv"))
    Temp_data_TSW['date'] = pd.DataFrame({'Hours': pd.date_range('2016-01-01', '2016-12-31', freq='15min')})
    Temp_data_TSW.set_index('date',inplace=True)
    Data_TSW.append(Temp_data_TSW)
    for l in range (0,len(TSW)):
        TSW_state.loc[:,'TSW'+str(l)] = TSW[l]['state']
    Temp_charge_TSW = pd.read_csv(os.path.join(file_path_TSW,"bev_time_series.csv"),header=([0]),skiprows=[1,2,3])
    Temp_charge_TSW['date'] =  pd.DataFrame({'Hours': pd.date_range('2016-01-01', '2016-12-31', freq='1H')})
    Temp_charge_TSW = Temp_charge_TSW[['date', 'balanced_MWh', 'immediate_MWh', 'from_23_to_8_at_any_MWh', 'from_0_to_24_at_home_MWh']]
    Temp_charge_TSW.set_index('date',inplace=True)
    Temp_charge_TSW = Temp_charge_TSW.resample('15min').ffill()
    Charge_TSW.append(Temp_charge_TSW)
    Temp_TSW = pd.concat([Temp_data_TSW,Temp_charge_TSW],axis=1)
    TSW.append(Temp_TSW)
    Temp_TSW_home = Temp_TSW[Temp_TSW['state'].str.contains('home')]
    Temp_TSW_home = Temp_TSW_home.fillna(0)
    TSW_home.append(Temp_TSW_home)
    # for j in range (len(TSW)):
    #     globals()[f"TSW{j}"] = TSW[j]
    #     TSW[j].to_csv(os.path.join(path2,'TSW'+str(j)+'.csv'))
    for k in range (len(TSW)):
        TSW_balanced.loc[:,'TSWB'+str(k)] = TSW[k]['balanced_MWh']
        TSW_uncontrolled.loc[:,'TSWU'+str(k)] = TSW[k]['immediate_MWh']
        TSW_nightcharge.loc[:,'TSWNC'+str(k)] = TSW[k]['from_23_to_8_at_any_MWh']
        TSW_home_balanced.loc[:,'TSWB'+str(k)] = TSW_home[k]['balanced_MWh']
        TSW_home_uncontrolled.loc[:,'TSWU'+str(k)] = TSW_home[k]['immediate_MWh']
        TSW_home_nightcharge.loc[:,'TSWNC'+str(k)] = TSW_home[k]['from_23_to_8_at_any_MWh']


#%% Tesla model 3 - Inactive 
Data_T3I = list()
Charge_T3I = list()
T3I = list()
T3I_home = list()
T3I_balanced = pd.DataFrame()
T3I_uncontrolled = pd.DataFrame()
T3I_nightcharge = pd.DataFrame()
T3I_home_balanced = pd.DataFrame()
T3I_home_uncontrolled = pd.DataFrame()
T3I_home_nightcharge = pd.DataFrame()
T3I_state = pd.DataFrame()

for i in range (1,T3_inactive+1):
    file_path_T3I = os.path.join(path,'T3','inactive'+str(i))
    Temp_data_T3I = pd.read_csv(os.path.join(file_path_T3I,"All_data.csv"))
    Temp_data_T3I['date'] = pd.DataFrame({'Hours': pd.date_range('2016-01-01', '2016-12-31', freq='15min')})
    Temp_data_T3I.set_index('date',inplace=True)
    Data_T3I.append(Temp_data_T3I)
    for l in range (0,len(T3I)):
        T3I_state.loc[:,'T3I'+str(l)] = T3I[l]['state']
    Temp_charge_T3I = pd.read_csv(os.path.join(file_path_T3I,"bev_time_series.csv"),header=([0]),skiprows=[1,2,3])
    Temp_charge_T3I['date'] =  pd.DataFrame({'Hours': pd.date_range('2016-01-01', '2016-12-31', freq='1H')})
    Temp_charge_T3I = Temp_charge_T3I[['date', 'balanced_MWh', 'immediate_MWh', 'from_23_to_8_at_any_MWh', 'from_0_to_24_at_home_MWh']]
    Temp_charge_T3I.set_index('date',inplace=True)
    Temp_charge_T3I = Temp_charge_T3I.resample('15min').ffill()
    Charge_T3I.append(Temp_charge_T3I)
    Temp_T3I = pd.concat([Temp_data_T3I,Temp_charge_T3I],axis=1)
    T3I.append(Temp_T3I)
    Temp_T3I_home = Temp_T3I[Temp_T3I['state'].str.contains('home')]
    Temp_T3I_home = Temp_T3I_home.fillna(0)
    T3I_home.append(Temp_T3I_home)
    # for j in range (len(T3I)):
    #     globals()[f"T3I{j}"] = T3I[j]
    #     T3I[j].to_csv(os.path.join(path2,'T3I'+str(j)+'.csv'))
    for k in range (len(T3I)):
        T3I_balanced.loc[:,'T3IB'+str(k)] = T3I[k]['balanced_MWh']
        T3I_uncontrolled.loc[:,'T3IU'+str(k)] = T3I[k]['immediate_MWh']
        T3I_nightcharge.loc[:,'T3INC'+str(k)] = T3I[k]['from_23_to_8_at_any_MWh']
        T3I_home_balanced.loc[:,'T3IB'+str(k)] = T3I_home[k]['balanced_MWh']
        T3I_home_uncontrolled.loc[:,'T3IU'+str(k)] = T3I_home[k]['immediate_MWh']
        T3I_home_nightcharge.loc[:,'T3INC'+str(k)] = T3I_home[k]['from_23_to_8_at_any_MWh']


#%% Tesla model 3 - Working
Data_T3W = list()
Charge_T3W = list()
T3W = list()
T3W_home = list()
T3W_balanced = pd.DataFrame()
T3W_uncontrolled = pd.DataFrame()
T3W_nightcharge = pd.DataFrame()
T3W_home_balanced = pd.DataFrame()
T3W_home_uncontrolled = pd.DataFrame()
T3W_home_nightcharge = pd.DataFrame()
T3W_state = pd.DataFrame()

for i in range (1,T3_working+1):
    file_path_T3W = os.path.join(path,'T3','working'+str(i))
    Temp_data_T3W = pd.read_csv(os.path.join(file_path_T3W,"All_data.csv"))
    Temp_data_T3W['date'] = pd.DataFrame({'Hours': pd.date_range('2016-01-01', '2016-12-31', freq='15min')})
    Temp_data_T3W.set_index('date',inplace=True)
    Data_T3W.append(Temp_data_T3W)
    for l in range (0,len(T3W)):
        T3W_state.loc[:,'T3W'+str(l)] = T3W[l]['state']
    Temp_charge_T3W = pd.read_csv(os.path.join(file_path_T3W,"bev_time_series.csv"),header=([0]),skiprows=[1,2,3])
    Temp_charge_T3W['date'] =  pd.DataFrame({'Hours': pd.date_range('2016-01-01', '2016-12-31', freq='1H')})
    Temp_charge_T3W = Temp_charge_T3W[['date', 'balanced_MWh', 'immediate_MWh', 'from_23_to_8_at_any_MWh', 'from_0_to_24_at_home_MWh']]
    Temp_charge_T3W.set_index('date',inplace=True)
    Temp_charge_T3W = Temp_charge_T3W.resample('15min').ffill()
    Charge_T3W.append(Temp_charge_T3W)
    Temp_T3W = pd.concat([Temp_data_T3W,Temp_charge_T3W],axis=1)
    T3W.append(Temp_T3W)
    Temp_T3W_home = Temp_T3W[Temp_T3W['state'].str.contains('home')]
    Temp_T3W_home = Temp_T3W_home.fillna(0)
    T3W_home.append(Temp_T3W_home)
    # for j in range (len(T3W)):
    #     globals()[f"T3W{j}"] = T3W[j]
    #     T3W[j].to_csv(os.path.join(path2,'T3W'+str(j)+'.csv'))
    for k in range (len(T3W)):
        T3W_balanced.loc[:,'T3WB'+str(k)] = T3W[k]['balanced_MWh']
        T3W_uncontrolled.loc[:,'T3WU'+str(k)] = T3W[k]['immediate_MWh']
        T3W_nightcharge.loc[:,'T3WNC'+str(k)] = T3W[k]['from_23_to_8_at_any_MWh']
        T3W_home_balanced.loc[:,'T3WB'+str(k)] = T3W_home[k]['balanced_MWh']
        T3W_home_uncontrolled.loc[:,'T3WU'+str(k)] = T3W_home[k]['immediate_MWh']
        T3W_home_nightcharge.loc[:,'T3WNC'+str(k)] = T3W_home[k]['from_23_to_8_at_any_MWh']

#%% Renault Zoe - Inactive 
Data_RZI = list()
Charge_RZI = list()
RZI = list()
RZI_home = list()
RZI_balanced = pd.DataFrame()
RZI_uncontrolled = pd.DataFrame()
RZI_nightcharge = pd.DataFrame()
RZI_home_balanced = pd.DataFrame()
RZI_home_uncontrolled = pd.DataFrame()
RZI_home_nightcharge = pd.DataFrame()
RZI_state = pd.DataFrame()

for i in range (1,RZ_inactive+1):
    file_path_RZI = os.path.join(path,'RZ','inactive'+str(i))
    Temp_data_RZI = pd.read_csv(os.path.join(file_path_RZI,"All_data.csv"))
    Temp_data_RZI['date'] = pd.DataFrame({'Hours': pd.date_range('2016-01-01', '2016-12-31', freq='15min')})
    Temp_data_RZI.set_index('date',inplace=True)
    Data_RZI.append(Temp_data_RZI)
    for l in range (0,len(RZI)):
        RZI_state.loc[:,'RZI'+str(l)] = RZI[l]['state']
    Temp_charge_RZI = pd.read_csv(os.path.join(file_path_RZI,"bev_time_series.csv"),header=([0]),skiprows=[1,2,3])
    Temp_charge_RZI['date'] =  pd.DataFrame({'Hours': pd.date_range('2016-01-01', '2016-12-31', freq='1H')})
    Temp_charge_RZI = Temp_charge_RZI[['date', 'balanced_MWh', 'immediate_MWh', 'from_23_to_8_at_any_MWh', 'from_0_to_24_at_home_MWh']]
    Temp_charge_RZI.set_index('date',inplace=True)
    Temp_charge_RZI = Temp_charge_RZI.resample('15min').ffill()
    Charge_RZI.append(Temp_charge_RZI)
    Temp_RZI = pd.concat([Temp_data_RZI,Temp_charge_RZI],axis=1)
    RZI.append(Temp_RZI)
    Temp_RZI_home = Temp_RZI[Temp_RZI['state'].str.contains('home')]
    Temp_RZI_home = Temp_RZI_home.fillna(0)
    RZI_home.append(Temp_RZI_home)
    # for j in range (len(RZI)):
    #     globals()[f"RZI{j}"] = RZI[j]
    #     RZI[j].to_csv(os.path.join(path2,'RZI'+str(j)+'.csv'))
    for k in range (len(RZI)):
        RZI_balanced.loc[:,'RZIB'+str(k)] = RZI[k]['balanced_MWh']
        RZI_uncontrolled.loc[:,'RZIU'+str(k)] = RZI[k]['immediate_MWh']
        RZI_nightcharge.loc[:,'RZINC'+str(k)] = RZI[k]['from_23_to_8_at_any_MWh']
        RZI_home_balanced.loc[:,'RZIB'+str(k)] = RZI_home[k]['balanced_MWh']
        RZI_home_uncontrolled.loc[:,'RZIU'+str(k)] = RZI_home[k]['immediate_MWh']
        RZI_home_nightcharge.loc[:,'RZINC'+str(k)] = RZI_home[k]['from_23_to_8_at_any_MWh']


#%% Renault Zoe - Working
Data_RZW = list()
Charge_RZW = list()
RZW = list()
RZW_home = list()
RZW_balanced = pd.DataFrame()
RZW_uncontrolled = pd.DataFrame()
RZW_nightcharge = pd.DataFrame()
RZW_home_balanced = pd.DataFrame()
RZW_home_uncontrolled = pd.DataFrame()
RZW_home_nightcharge = pd.DataFrame()
RZW_state = pd.DataFrame()

for i in range (1,RZ_working+1):
    file_path_RZW = os.path.join(path,'RZ','working'+str(i))
    Temp_data_RZW = pd.read_csv(os.path.join(file_path_RZW,"All_data.csv"))
    Temp_data_RZW['date'] = pd.DataFrame({'Hours': pd.date_range('2016-01-01', '2016-12-31', freq='15min')})
    Temp_data_RZW.set_index('date',inplace=True)
    Data_RZW.append(Temp_data_RZW)
    for l in range (0,len(RZW)):
        RZW_state.loc[:,'RZW'+str(l)] = RZW[l]['state']
    Temp_charge_RZW = pd.read_csv(os.path.join(file_path_RZW,"bev_time_series.csv"),header=([0]),skiprows=[1,2,3])
    Temp_charge_RZW['date'] =  pd.DataFrame({'Hours': pd.date_range('2016-01-01', '2016-12-31', freq='1H')})
    Temp_charge_RZW = Temp_charge_RZW[['date', 'balanced_MWh', 'immediate_MWh', 'from_23_to_8_at_any_MWh', 'from_0_to_24_at_home_MWh']]
    Temp_charge_RZW.set_index('date',inplace=True)
    Temp_charge_RZW = Temp_charge_RZW.resample('15min').ffill()
    Charge_RZW.append(Temp_charge_RZW)
    Temp_RZW = pd.concat([Temp_data_RZW,Temp_charge_RZW],axis=1)
    RZW.append(Temp_RZW)
    Temp_RZW_home = Temp_RZW[Temp_RZW['state'].str.contains('home')]
    Temp_RZW_home = Temp_RZW_home.fillna(0)
    RZW_home.append(Temp_RZW_home)
    # for j in range (len(RZW)):
    #     globals()[f"RZW{j}"] = RZW[j]
    #     RZW[j].to_csv(os.path.join(path2,'RZW'+str(j)+'.csv'))
    for k in range (len(RZW)):
        RZW_balanced.loc[:,'RZWB'+str(k)] = RZW[k]['balanced_MWh']
        RZW_uncontrolled.loc[:,'RZWU'+str(k)] = RZW[k]['immediate_MWh']
        RZW_nightcharge.loc[:,'RZWNC'+str(k)] = RZW[k]['from_23_to_8_at_any_MWh']
        RZW_home_balanced.loc[:,'RZWB'+str(k)] = RZW_home[k]['balanced_MWh']
        RZW_home_uncontrolled.loc[:,'RZWU'+str(k)] = RZW_home[k]['immediate_MWh']
        RZW_home_nightcharge.loc[:,'RZWNC'+str(k)] = RZW_home[k]['from_23_to_8_at_any_MWh']

#%% Hyundai Kona - Inactive 
Data_HKI = list()
Charge_HKI = list()
HKI = list()
HKI_home = list()
HKI_balanced = pd.DataFrame()
HKI_uncontrolled = pd.DataFrame()
HKI_nightcharge = pd.DataFrame()
HKI_home_balanced = pd.DataFrame()
HKI_home_uncontrolled = pd.DataFrame()
HKI_home_nightcharge = pd.DataFrame()
HKI_state = pd.DataFrame()

for i in range (1,HK_inactive+1):
    file_path_HKI = os.path.join(path,'HK','inactive'+str(i))
    Temp_data_HKI = pd.read_csv(os.path.join(file_path_HKI,"All_data.csv"))
    Temp_data_HKI['date'] = pd.DataFrame({'Hours': pd.date_range('2016-01-01', '2016-12-31', freq='15min')})
    Temp_data_HKI.set_index('date',inplace=True)
    Data_HKI.append(Temp_data_HKI)
    for l in range (0,len(HKI)):
        HKI_state.loc[:,'HKI'+str(l)] = HKI[l]['state']
    Temp_charge_HKI = pd.read_csv(os.path.join(file_path_HKI,"bev_time_series.csv"),header=([0]),skiprows=[1,2,3])
    Temp_charge_HKI['date'] =  pd.DataFrame({'Hours': pd.date_range('2016-01-01', '2016-12-31', freq='1H')})
    Temp_charge_HKI = Temp_charge_HKI[['date', 'balanced_MWh', 'immediate_MWh', 'from_23_to_8_at_any_MWh', 'from_0_to_24_at_home_MWh']]
    Temp_charge_HKI.set_index('date',inplace=True)
    Temp_charge_HKI = Temp_charge_HKI.resample('15min').ffill()
    Charge_HKI.append(Temp_charge_HKI)
    Temp_HKI = pd.concat([Temp_data_HKI,Temp_charge_HKI],axis=1)
    HKI.append(Temp_HKI)
    Temp_HKI_home = Temp_HKI[Temp_HKI['state'].str.contains('home')]
    Temp_HKI_home = Temp_HKI_home.fillna(0)
    HKI_home.append(Temp_HKI_home)
    # Fleet.append(Temp_HKI)
    # for j in range (len(HKI)):
    #     globals()[f"HKI{j}"] = HKI[j]
    #     HKI[j].to_csv(os.path.join(path2,'HKI'+str(j)+'.csv'))
    for k in range (len(HKI)):
        HKI_balanced.loc[:,'HKIB'+str(k)] = HKI[k]['balanced_MWh']
        HKI_uncontrolled.loc[:,'HKIU'+str(k)] = HKI[k]['immediate_MWh']
        HKI_nightcharge.loc[:,'HKINC'+str(k)] = HKI[k]['from_23_to_8_at_any_MWh']
        HKI_home_balanced.loc[:,'HKIB'+str(k)] = HKI_home[k]['balanced_MWh']
        HKI_home_uncontrolled.loc[:,'HKIU'+str(k)] = HKI_home[k]['immediate_MWh']
        HKI_home_nightcharge.loc[:,'HKINC'+str(k)] = HKI_home[k]['from_23_to_8_at_any_MWh']

#%% Hyundai Kona - Working
Data_HKW = list()
Charge_HKW = list()
HKW = list()
HKW_home = list()
HKW_balanced = pd.DataFrame()
HKW_uncontrolled = pd.DataFrame()
HKW_nightcharge = pd.DataFrame()
HKW_home_balanced = pd.DataFrame()
HKW_home_uncontrolled = pd.DataFrame()
HKW_home_nightcharge = pd.DataFrame()
HKW_state = pd.DataFrame()

for i in range (1,HK_working+1):
    file_path_HKW = os.path.join(path,'HK','working'+str(i))
    Temp_data_HKW = pd.read_csv(os.path.join(file_path_HKW,"All_data.csv"))
    Temp_data_HKW['date'] = pd.DataFrame({'Hours': pd.date_range('2016-01-01', '2016-12-31', freq='15min')})
    Temp_data_HKW.set_index('date',inplace=True)
    Data_HKW.append(Temp_data_HKW)
    for l in range (0,len(HKW)):
        HKW_state.loc[:,'HKW'+str(l)] = HKW[l]['state']
    Temp_charge_HKW = pd.read_csv(os.path.join(file_path_HKW,"bev_time_series.csv"),header=([0]),skiprows=[1,2,3])
    Temp_charge_HKW['date'] =  pd.DataFrame({'Hours': pd.date_range('2016-01-01', '2016-12-31', freq='1H')})
    Temp_charge_HKW = Temp_charge_HKW[['date', 'balanced_MWh', 'immediate_MWh', 'from_23_to_8_at_any_MWh', 'from_0_to_24_at_home_MWh']]
    Temp_charge_HKW.set_index('date',inplace=True)
    Temp_charge_HKW = Temp_charge_HKW.resample('15min').ffill()
    Charge_HKW.append(Temp_charge_HKW)
    Temp_HKW = pd.concat([Temp_data_HKW,Temp_charge_HKW],axis=1)
    HKW.append(Temp_HKW)
    Temp_HKW_home = Temp_HKW[Temp_HKI['state'].str.contains('home')]
    Temp_HKW_home = Temp_HKW_home.fillna(0)
    HKW_home.append(Temp_HKW_home)
    # Fleet.append(Temp_HKW)
    # for j in range (len(HKW)):
    #     globals()[f"HKW{j}"] = HKW[j]
    #     HKW[j].to_csv(os.path.join(path2,'HKW'+str(j)+'.csv'))
    for k in range (len(HKW)):
        HKW_balanced.loc[:,'HKWB'+str(k)] = HKW[k]['balanced_MWh']
        HKW_uncontrolled.loc[:,'HKWU'+str(k)] = HKW[k]['immediate_MWh']
        HKW_nightcharge.loc[:,'HKWNC'+str(k)] = HKW[k]['from_23_to_8_at_any_MWh']
        HKW_home_balanced.loc[:,'HKWB'+str(k)] = HKW_home[k]['balanced_MWh']
        HKW_home_uncontrolled.loc[:,'HKWU'+str(k)] = HKW_home[k]['immediate_MWh']
        HKW_home_nightcharge.loc[:,'HKWNC'+str(k)] = HKW_home[k]['from_23_to_8_at_any_MWh']

#del Temp_HKI, Temp_HKI_home, Temp_HKW, Temp_HKW_home, Temp_RZI, Temp_RZI_home, Temp_RZW, Temp_RZW_home, Temp_T3I, Temp_T3I_home, Temp_T3W, Temp_T3W_home, Temp_TSI, Temp_TSI_home, Temp_TSW, Temp_TSW_home, Temp_charge_HKI, Temp_charge_HKW, Temp_charge_RZI, Temp_charge_RZW, Temp_charge_T3I, Temp_charge_T3W, Temp_charge_TSI, Temp_charge_TSW, Temp_data_HKI, Temp_data_HKW, Temp_data_RZI, Temp_data_RZW, Temp_data_T3I, Temp_data_T3W, Temp_data_TSI, Temp_data_TSW

#%% Creation of the fleet 
Fleet_TSW = TSW_balanced.iloc[:, 0:EV_TSW_balanced].sum(axis=1) + TSW_uncontrolled.iloc[:, EV_TSW_balanced:(EV_TSW_balanced+EV_TSW_uncontrolled)].sum(axis=1) + TSW_nightcharge.iloc[:, (EV_TSW_balanced+EV_TSW_uncontrolled):(EV_TSW_balanced+EV_TSW_uncontrolled+EV_TSW_nightcharge)].sum(axis=1)
Fleet_TSI = TSI_balanced.iloc[:, 0:EV_TSI_balanced].sum(axis=1) + TSI_uncontrolled.iloc[:, EV_TSI_balanced:(EV_TSI_balanced+EV_TSI_uncontrolled)].sum(axis=1) + TSI_nightcharge.iloc[:, (EV_TSI_balanced+EV_TSI_uncontrolled):(EV_TSI_balanced+EV_TSI_uncontrolled+EV_TSI_nightcharge)].sum(axis=1)
Fleet_T3W = T3W_balanced.iloc[:, 0:EV_T3W_balanced].sum(axis=1) + T3W_uncontrolled.iloc[:, EV_T3W_balanced:(EV_T3W_balanced+EV_T3W_uncontrolled)].sum(axis=1) + T3W_nightcharge.iloc[:, (EV_T3W_balanced+EV_T3W_uncontrolled):(EV_T3W_balanced+EV_T3W_uncontrolled+EV_T3W_nightcharge)].sum(axis=1)
Fleet_T3I = T3I_balanced.iloc[:, 0:EV_T3I_balanced].sum(axis=1) + T3I_uncontrolled.iloc[:, EV_T3I_balanced:(EV_T3I_balanced+EV_T3I_uncontrolled)].sum(axis=1) + T3I_nightcharge.iloc[:, (EV_T3I_balanced+EV_T3I_uncontrolled):(EV_T3I_balanced+EV_T3I_uncontrolled+EV_T3I_nightcharge)].sum(axis=1)
Fleet_RZW = RZW_balanced.iloc[:, 0:EV_RZW_balanced].sum(axis=1) + RZW_uncontrolled.iloc[:, EV_RZW_balanced:(EV_RZW_balanced+EV_RZW_uncontrolled)].sum(axis=1) + RZW_nightcharge.iloc[:, (EV_RZW_balanced+EV_RZW_uncontrolled):(EV_RZW_balanced+EV_RZW_uncontrolled+EV_RZW_nightcharge)].sum(axis=1)
Fleet_RZI = RZI_balanced.iloc[:, 0:EV_RZI_balanced].sum(axis=1) + RZI_uncontrolled.iloc[:, EV_RZI_balanced:(EV_RZI_balanced+EV_RZI_uncontrolled)].sum(axis=1) + RZI_nightcharge.iloc[:, (EV_RZI_balanced+EV_RZI_uncontrolled):(EV_RZI_balanced+EV_RZI_uncontrolled+EV_RZI_nightcharge)].sum(axis=1)
Fleet_HKW = HKW_balanced.iloc[:, 0:EV_HKW_balanced].sum(axis=1) + HKW_uncontrolled.iloc[:, EV_HKW_balanced:(EV_HKW_balanced+EV_HKW_uncontrolled)].sum(axis=1) + HKW_nightcharge.iloc[:, (EV_HKW_balanced+EV_HKW_uncontrolled):(EV_HKW_balanced+EV_HKW_uncontrolled+EV_HKW_nightcharge)].sum(axis=1) 
Fleet_HKI = HKI_balanced.iloc[:, 0:EV_HKI_balanced].sum(axis=1) + HKI_uncontrolled.iloc[:, EV_HKI_balanced:(EV_HKI_balanced+EV_HKI_uncontrolled)].sum(axis=1) + HKI_nightcharge.iloc[:, (EV_HKI_balanced+EV_HKI_uncontrolled):(EV_HKI_balanced+EV_HKI_uncontrolled+EV_HKI_nightcharge)].sum(axis=1)

Fleet_15min = pd.concat([Fleet_TSW,Fleet_TSI,Fleet_T3W,Fleet_T3I,Fleet_RZW,Fleet_RZI,Fleet_HKW,Fleet_HKI],axis=1).fillna(0).sum(axis=1)
Fleet_15min.index.names = ['date']

#Total of the fleet 
Fleet_MWh = Fleet_15min.resample('h').mean()
Total_fleet_MWh = Fleet_MWh.sum()

#Create fleet at home and replace nan values for resample 
Fleet_TSW_home = TSW_home_balanced.iloc[:, 0:EV_TSW_balanced].sum(axis=1) + TSW_home_uncontrolled.iloc[:, EV_TSW_balanced:(EV_TSW_balanced+EV_TSW_uncontrolled)].sum(axis=1) + TSW_home_nightcharge.iloc[:, (EV_TSW_balanced+EV_TSW_uncontrolled):(EV_TSW_balanced+EV_TSW_uncontrolled+EV_TSW_nightcharge)].sum(axis=1) 
Fleet_TSI_home = TSI_home_balanced.iloc[:, 0:EV_TSI_balanced].sum(axis=1) + TSI_home_uncontrolled.iloc[:, EV_TSI_balanced:(EV_TSI_balanced+EV_TSI_uncontrolled)].sum(axis=1) + TSI_home_nightcharge.iloc[:, (EV_TSI_balanced+EV_TSI_uncontrolled):(EV_TSI_balanced+EV_TSI_uncontrolled+EV_TSI_nightcharge)].sum(axis=1)
Fleet_T3W_home = T3W_home_balanced.iloc[:, 0:EV_T3W_balanced].sum(axis=1) + T3W_home_uncontrolled.iloc[:, EV_T3W_balanced:(EV_T3W_balanced+EV_T3W_uncontrolled)].sum(axis=1) + T3W_home_nightcharge.iloc[:, (EV_T3W_balanced+EV_T3W_uncontrolled):(EV_T3W_balanced+EV_T3W_uncontrolled+EV_T3W_nightcharge)].sum(axis=1)
Fleet_T3I_home = T3I_home_balanced.iloc[:, 0:EV_T3I_balanced].sum(axis=1) + T3I_home_uncontrolled.iloc[:, EV_T3I_balanced:(EV_T3I_balanced+EV_T3I_uncontrolled)].sum(axis=1) + T3I_home_nightcharge.iloc[:, (EV_T3I_balanced+EV_T3I_uncontrolled):(EV_T3I_balanced+EV_T3I_uncontrolled+EV_T3I_nightcharge)].sum(axis=1)
Fleet_RZW_home = RZW_home_balanced.iloc[:, 0:EV_RZW_balanced].sum(axis=1) + RZW_home_uncontrolled.iloc[:, EV_RZW_balanced:(EV_RZW_balanced+EV_RZW_uncontrolled)].sum(axis=1) + RZW_home_nightcharge.iloc[:, (EV_RZW_balanced+EV_RZW_uncontrolled):(EV_RZW_balanced+EV_RZW_uncontrolled+EV_RZW_nightcharge)].sum(axis=1)
Fleet_RZI_home = RZI_home_balanced.iloc[:, 0:EV_RZI_balanced].sum(axis=1) + RZI_home_uncontrolled.iloc[:, EV_RZI_balanced:(EV_RZI_balanced+EV_RZI_uncontrolled)].sum(axis=1) + RZI_home_nightcharge.iloc[:, (EV_RZI_balanced+EV_RZI_uncontrolled):(EV_RZI_balanced+EV_RZI_uncontrolled+EV_RZI_nightcharge)].sum(axis=1)
Fleet_HKW_home = HKW_home_balanced.iloc[:, 0:EV_HKW_balanced].sum(axis=1) + HKW_home_uncontrolled.iloc[:, EV_HKW_balanced:(EV_HKW_balanced+EV_HKW_uncontrolled)].sum(axis=1) + HKW_home_nightcharge.iloc[:, (EV_HKW_balanced+EV_HKW_uncontrolled):(EV_HKW_balanced+EV_HKW_uncontrolled+EV_HKW_nightcharge)].sum(axis=1)
Fleet_HKI_home = HKI_home_balanced.iloc[:, 0:EV_HKI_balanced].sum(axis=1) + HKI_home_uncontrolled.iloc[:, EV_HKI_balanced:(EV_HKI_balanced+EV_HKI_uncontrolled)].sum(axis=1) + HKI_home_nightcharge.iloc[:, (EV_HKI_balanced+EV_HKI_uncontrolled):(EV_HKI_balanced+EV_HKI_uncontrolled+EV_HKI_nightcharge)].sum(axis=1)

Fleet_home_15min = pd.concat([Fleet_TSW_home,Fleet_TSI_home,Fleet_T3W_home,Fleet_T3I_home,Fleet_RZW_home,Fleet_RZI_home,Fleet_HKW_home,Fleet_HKI_home],axis=1).fillna(0).sum(axis=1)
Fleet_home_15min.index.names = ['date']

#Total of the fleet at home
Fleet_home_MWh = Fleet_home_15min.resample('h').mean()
Total_fleet_home_MWh = Fleet_home_MWh.sum()

#State of the fleet
Fleet_state = pd.concat([TSI_state, TSW_state, T3I_state, T3W_state, RZI_state, RZW_state, HKI_state, HKW_state], axis=1)
Fleet_state.index.names = ['date']

#%% Export the charging demand of the fleet for further analysis 
output_path = os.path.join(r'C:\Users\janva\Emobpy\example\db','Fleets',Output_name+".csv")
output_path_home = os.path.join(r'C:\Users\janva\Emobpy\example\db','Fleets',Output_name+"_home.csv")
output_path_state = os.path.join(r'C:\Users\janva\Emobpy\example\db','Fleets',Output_name+"_state.csv")

Fleet_MWh.to_csv(output_path)
Fleet_home_MWh.to_csv(output_path_home)
Fleet_state.to_csv(output_path_state)



# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 13:38:58 2022

@author: janva
"""
## Vehicle mobility time series 
# Initialize seed. Seed can be used to continue on the same generated profile
# from emobpy.tools import set_seed
# set_seed(dir=r'C:\Users\janva\Emobpy\example\config_files/')

from emobpy import Mobility
from emobpy.constants import RULE; RULE
from emobpy import DataBase
from emobpy import Consumption, HeatInsulation, BEVspecs
from emobpy import Availability
from emobpy import Charging
from emobpy import Export
import os


#Set simulation parameters
"""
Activity types = working/inactive
EV types = Renault Zoe (RZ), Tesla model 3 (T3), Tesla model S (TS), Hyundai Kona (HK)""" 

activity = 'inactive'
EVs = 2
EV_type = 'RZ'


folder = 1
while (folder<=EVs):
    path = r'C:\Users\janva\Emobpy\example\db\test'
    file_path = os.path.join(path,EV_type,activity+str(folder))
    inactive_working = os.path.join("DepartureDestinationTrip_"+activity+".csv")
    
    m = Mobility(config_folder=r'C:\Users\janva\Emobpy\example\config_files/')

    m.set_params(
                 name_prefix="BEV1",
                 total_hours=365*24, # one year
                 time_step_in_hrs=0.25, # 15 minutes
                 category="user_defined",
                 reference_date="01/01/2016"
                 )

    m.set_stats(
                stat_ntrip_path="TripsPerDay.csv",
                stat_dest_path=inactive_working,
                stat_km_duration_path="DistanceDurationTrip.csv",
                )

    m.set_rules(rule_key="user_defined") # see /config_files/rules.yml, it contains a dictionary
                                     # whose key must be the same as rule_key. 
    m.run()


    m.save_profile(folder=file_path)

    #Mobility dataframes
    mobility_TS = m.timeseries
    mobility_profile = m.profile


    DB = DataBase(file_path)
    DB.loadfiles()
    DB.db.keys()


    ## Driving consumption time series
    DB.update()                          # This load new files hosted in database folder as result of new generated files
    # mname = list(DB.db.keys())[0]      # getting the id of the first mobility profile
    mname = m.name
    HI = HeatInsulation(True)            # Creating the heat insulation by copying the default configuration
    BEVS = BEVspecs()                    # Database that contains BEV models

    #Also change the EV type here
    R_Zoe = BEVS.model(('Renault','Zoe Q90',2019))
    #Tesla_3 = BEVS.model(('Tesla','Model 3 Standard Range RWD',2019))
    #Tesla_S = BEVS.model(('Tesla','Model S 60 RWD',2015))
    #H_Kona = BEVS.model(('Hyundai','KONA Electric 64 kWh',2019))


    c = Consumption(mname, R_Zoe)        # And change the EV type here
    c.load_setting_mobility(DB)

    ## Download and import weather file if needed 
    #from emobpy import Weather 
    #WD = Weather()
    #WD.download_weather_data()

    c.run(
      heat_insulation=HI,
      weather_country='NL',
      weather_year=2016,
      passenger_mass=75,                   # kg
      passenger_sensible_heat=70,          # W
      passenger_nr=1.5,                    # Passengers per vehicle including driver
      air_cabin_heat_transfer_coef=20,     # W/(m2K). Interior walls
      air_flow = 0.02,                     # m3/s. Ventilation
      driving_cycle_type='WLTC',           # Two options "WLTC" or "EPA"
      road_type=0,                         # For rolling resistance, Zero represents a new road.
      road_slope=0
      )

    c.save_profile(file_path)

    #Dataframes
    consumption_TS = c.timeseries # Consumption in kWh/timestep -> timestep 15 min in this example
    consumption_profile = c.profile.head()


    ## Grid availability time series 
    DB.update()                               # This load new generated files that are hosted in database folder
    cname = c.name                            # getting the id of the first consumption profile


    station_distribution = {                  # Dictionary with charging stations type probability distribution per the purpose of the trip (location or destination)
                            'prob_charging_point': {
                                'errands': {'public': 0.8, 'none': 0.2},
                                'escort': {'public': 0.8, 'none': 0.2},
                                'leisure': {'public': 0.8, 'none': 0.2},
                                'shopping': {'public': 0.8, 'none': 0.2},
                                'home': {'public': 0.0, 'none': 0.2, 'home': 0.8},
                                'workplace': {'public': 0.0, 'workplace': 0.0, 'none': 1.0},   # If the vehicle is at the workplace, it will always find a charging station available (assumption)
                                'driving': {'none': 0.99, 'fast75': 0.005, 'fast150': 0.005}}, # with the low probability given to fast charging is to ensure fast charging only for very long trips (assumption)
                            'capacity_charging_point': {                                       # Nominal power rating of charging station in kW
                                                        'public': 22,
                                                        'home': 3.7,
                                                        'workplace': 11,
                                                        'none': 0,  # dummy station
                                                        'fast75': 150,
                                                        'fast150': 150}
                            }

    ga = Availability(cname, DB)
    ga.set_scenario(station_distribution)


    ga.run()
    ga.save_profile(file_path)

    #Dataframes 
    availability_TS = ga.timeseries
    availability_profile = ga.profile


    ## Grid electricity demand 
    DB.update()

    aname = ga.name                            # getting the id of the availability profile

    strategies = [
                  "immediate",                 # When battery has SOC < 100% then it charges immediatelly at a maximun power rating of the current charging station
                  "balanced",                  # When battery has SOC < 100% then it charges immediatelly but at lower rating power to ensure 100% SOC at the end (before moving to another place).
                  "from_0_to_24_at_home",      # Customized: starting time of charging (this case 0 hrs), final time of charging (this case 24 hrs), at could be one 'location' (this case 'home') or 'any'.
                  "from_23_to_8_at_any"
                  ]

    for option in strategies:
        ged = Charging(aname)
        ged.load_scenario(DB)
        ged.set_sub_scenario(option)
        ged.run()
        print(f'Creation Successful:{ged.success}')   # if False, modify the strategy to a less constrained.
        ged.save_profile(file_path)
    
    charging_TS = ged.timeseries
    charging_profile = ged.profile

    #All data in one DF
    file_path_alldata = os.path.join(path,EV_type,activity+str(folder),'All_data.csv')
    All_data = charging_TS.join(availability_TS[["soc"]])
    All_data = All_data.join(consumption_TS[["average power in W"]])
    All_data.to_csv(file_path_alldata)


    print (folder)
    DB.update()
    Exp = Export()
    Exp.loaddata(DB)
    Exp.to_csv()
    Exp.save_files(repository=file_path)
    folder = folder+1

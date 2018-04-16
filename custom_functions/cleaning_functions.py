#%% functions
import pandas as pd
import glob
import os
import re

#%%
def tsvs_from_folder(folder_path,meter_type='Electricity'):
    # get all filepaths in folder
    allfiles = glob.glob(folder_path+"/*.tab")
    
    # create a list with the name of each submeter
    name = [re.search('{}_(.*).tab$'.format(meter_type),fp).group(1) for fp in allfiles]

    # provided the file name and corresponding path to each file
    # read in file and parse datetime
    # store in dictionary of dataframes
    datadct = {}
    for k, v in zip(name,allfiles):
        print(k)
        datadct[k] = pd.read_csv(v,delimiter='\t',header=0)
        datadct[k]['ts'] = pd.to_datetime(datadct[k]['unix_ts'],unit='s')
        datadct[k].set_index('ts',inplace=True)
        datadct[k].drop('unix_ts',axis=1,inplace=True)

    # join everything together based on index        
    df = pd.concat(datadct,axis=1,join='outer')
    df.index.rename('ts',inplace=True)

    return df

def elec_clean(elec_folder_path):
    elec = tsvs_from_folder(elec_folder_path)

    # take only the "power" columns
    elec = elec.xs('P',level=1,axis=1).copy()

    # add extra columns based on documentation
    elec['MHE'] = elec['WHE'] - elec['RSE'] - elec['GRE']
    elec['UNE'] = elec['MHE'] - elec.drop(['MHE','WHE','RSE','GRE'],axis=1).sum(axis=1)

    # Rename columns
    actual_names = {
        'B1E':'north_br',
        'B2E':'south_br',
        'BME':'basement',
        'CDE':'dryer',
        'CWE':'washer',
        'DNE':'dining_room',
        'DWE':'dishwasher',
        'EBE':'workbench',
        'EQE':'security_system',
        'FGE':'refrigerator',
        'FRE':'furnace_fan',
        'GRE':'garage',
        'HPE':'heat_pump',
        'HTE':'dhw_heater',
        'MHE':'main_house_total',
        'OFE':'office',
        'OUE':'outside_plug',
        'RSE':'rental_suite',
        'TVE':'entertainment',
        'UTE':'utility_room',
        'UNE':'unmetered',
        'WHE':'whole_house_total',
        'WOE':'oven'}

    elec.rename(columns = actual_names,inplace=True)

    return elec

def weather_clean(weather_hourly_file_path):
    # import weather data
    weather = pd.read_csv(
        weather_hourly_file_path, 
        index_col=0, 
        delimiter='\t', 
        header=0, 
        parse_dates=True,
        usecols=['Date/Time','Temp (C)',
            'Dew Point Temp (C)',
            'Rel Hum (%)',
            'Wind Spd (km/h)',
            'Stn Press (kPa)'])

    weather.index.name = 'ts'
    weather.interpolate(method='time',axis=0,inplace=True)

    return weather


def elec_weather_merge(elec_folder_path, weather_hourly_file_path):

    elec = elec_clean(elec_folder_path)
    weather = weather_clean(weather_hourly_file_path)

    # dumb ass merge method
    elec['Year'] = elec .index.year
    elec['Month'] = elec.index.month
    elec['Day'] = elec.index.day
    elec['Hour'] = elec.index.hour
    weather['Year'] = weather.index.year
    weather['Month'] = weather.index.month
    weather['Day'] = weather.index.day
    weather['Hour'] = weather.index.hour
    ymdh = ['Year','Month','Day','Hour']
    merged = pd.merge(elec,weather,on=ymdh,how='left').drop(ymdh,axis=1)
    merged.index = elec.index
    merged.dropna(axis=0,inplace=True)

    return merged

if __name__ == "__main__":
    elec_folder_path = '/users/ianmyjer/desktop/disagg/elec/'
    weather_hourly_file_path = '/users/ianmyjer/desktop/disagg/weather/Climate_HourlyWeather.tab'

    elec_weather_merge(elec_folder_path, weather_hourly_file_path)


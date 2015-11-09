from ConfigParser import SafeConfigParser
import json
import time

import requests

# read config file for credentials
config = SafeConfigParser()
config.read('../config/credentials.conf')

## login at home.nest.com and get transport_url, access_token and userid
#headers = {'user-agent': 'Nest/1.1.0.10 CFNetwork/548.0.4'}
data = {'username': config.get('account','username'), 'password': config.get('account','password')}
#login_result = requests.post('https://home.nest.com/user/login', headers=headers, data=data)
login_result = requests.post('https://home.nest.com/user/login',  data=data)

## parse the results
login_result_json = login_result.json()
userid = login_result_json['userid']
access_token = login_result_json['access_token']
transport_url = login_result_json['urls']['transport_url']
weather_url = login_result_json['urls']['weather_url']

## DEBUG
#print('userid: {userid}'.format(userid = userid))
#print('access_token: {access_token}'.format(access_token = access_token))
#print('transport_url: {transport_url}'.format(transport_url = transport_url))
#print('weather_url: {weather_url}'.format(weather_url = weather_url))
## END DEBUG

## get thermostat data
authorization_headers = {'Authorization': 'Basic ' + access_token}
status = requests.get(transport_url + '/v2/mobile/user.' + userid, headers=authorization_headers)

## parse the results
status_json = status.json()
deviceid = status_json['device'].keys()[0]
auto_away = status_json['shared'][deviceid]['auto_away']
current_humidity = status_json['device'][deviceid]['current_humidity']
current_temperature = status_json['shared'][deviceid]['current_temperature']
target_temperature = status_json['shared'][deviceid]['target_temperature']
if(status_json['shared'][deviceid]['hvac_heater_state']):
    hvac_heater_state = 1
else:
    hvac_heater_state = 0

## DEBUG
#print('deviceid: {deviceid}'.format(deviceid = deviceid))
#print('auto_away: {auto_away}'.format(auto_away = auto_away))
#print('current_humidity: {current_humidity}'.format(current_humidity = current_humidity))
#print('current_temperature: {current_temperature}'.format(current_temperature = current_temperature))
#print('target_temperature: {target_temperature}'.format(target_temperature = target_temperature))
#print('heating: {hvac_heater_state}'.format(hvac_heater_state = hvac_heater_state))
## END DEBUG

## get weather data
city = config.get('location','city')
weather = requests.get(weather_url + city)

## parse weather data
weather_json = weather.json()
current_outside_humidity = weather_json[city]['current']['humidity']
current_outside_temperature = weather_json[city]['current']['temp_c']

## DEBUG
#print('current_outside_humidity: {current_outside_humidity}'.format(current_outside_humidity = current_outside_humidity))
#print('current_outside_temperature: {current_outside_temperature}'.format(current_outside_temperature = current_outside_temperature))
## END DEBUG

## write data to InfluxDB
nest_data = 'auto_away,owner={username} value={auto_away} {now}\ncurrent_humidity,owner={username} value={current_humidity} {now}\ncurrent_temperature,owner={username} value={current_temperature} {now}\ntarget_temperature,owner={username} value={target_temperature} {now}\nhvac_heater_state,owner={username} value={hvac_heater_state} {now}\ncurrent_outside_humidity,owner={username} value={current_outside_humidity} {now}\ncurrent_outside_temperature,owner={username} value={current_outside_temperature} {now}'.format(now = time.strftime('%s'), username = config.get('account','username'), auto_away = auto_away, current_humidity = current_humidity, current_temperature = current_temperature, target_temperature = target_temperature, hvac_heater_state = hvac_heater_state, current_outside_humidity = current_outside_humidity, current_outside_temperature = current_outside_temperature)
print(nest_data)
print(config.get('influxdb','host'))
print(config.get('influxdb','database'))
influxdb = requests.post('http://{influxdb_host}:8086/write?db={database}'.format(influxdb_host = config.get('influxdb','host'), database=config.get('influxdb','database')), data=nest_data)
print(influxdb.status_code)
print(influxdb.text)

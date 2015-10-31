from ConfigParser import SafeConfigParser
import json

import requests

# read config file for credentials
config = SafeConfigParser()
config.read('../config/credentials.conf')

# login at home.nest.com and get transport_url, access_token and userid
#headers = {'user-agent': 'Nest/1.1.0.10 CFNetwork/548.0.4'}
data = {'username': config.get('account', 'username'), 'password': config.get('account', 'password')}
#login_result = requests.post('https://home.nest.com/user/login', headers=headers, data=data)
login_result = requests.post('https://home.nest.com/user/login',  data=data)

## parse the results
login_result_json = login_result.json()
userid = login_result_json['userid']
access_token = login_result_json['access_token']
transport_url = login_result_json['urls']['transport_url']

print('userid: {userid}'.format(userid = userid))
print('access_token: {access_token}'.format(access_token = access_token))
print('transport_url: {transport_url}'.format(transport_url = transport_url))

authorization_headers = {'Authorization': 'Basic ' + access_token}
status = requests.get(transport_url + '/v2/mobile/user.' + userid, headers=authorization_headers)
print(status.status_code)
print(status.text)

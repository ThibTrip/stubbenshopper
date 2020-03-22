# -*- coding: utf-8 -*-
import requests

# # Config

base_url = "http://127.0.0.1:5000/"


# # Function for querying the API (so we don't repeat ourselves)

def send_request(endpoint, method, json_data, **kwargs):
    url = base_url.strip('/') + f'/{endpoint}'
    with requests.session() as session:
        response = session.request(method=method,
                                   url=url,
                                   json=json_data,
                                   **kwargs)
    return response


# # Test1: reseller subscribe with feedback

send_request(endpoint='subscribe', method='POST',
             json_data={'email':'thibault.betremieux@port-neo.com',
                        'user_category':'reseller', # OR "driver"
                        'zip_code':'79108',
                        'feedback':'wow this is really cool 🐓🐓! '}).json()

# # Test2: driver subscribe without feedback

send_request(endpoint='subscribe', method='POST',
             json_data={'email':'thibault.betremieux@gmail.com', 
                        'zip_code':'79108', 
                        'user_category':'driver'}).json()

# # Error codes

# ## 405 no JSON

send_request(endpoint='subscribe', method='POST', json_data=None).json()

# ## 406 missing keys

send_request(endpoint='subscribe', method='POST', json_data={'user_category':'driver'}).json()

# ## 407 user_category must be "driver" or "reseller"

send_request(endpoint='subscribe', method='POST', json_data={'email':'foobar@test.com', 
                                                             'zip_code':'79108',
                                                             'user_category':'banana'}).json()

# # 408 already subscribed

send_request(endpoint='subscribe', method='POST', json_data={'email':'thibault.betremieux@port-neo.com',
                                                             'zip_code':'79108',
                                                             'user_category':'driver'}).json()

# ## 409 invalid email address

send_request(endpoint='subscribe', method='POST', json_data={'email':'not_valid@@gmail.com',
                                                             'zip_code':'79108',
                                                             'user_category':'driver'}).json()

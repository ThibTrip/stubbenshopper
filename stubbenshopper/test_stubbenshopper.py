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


# # Signup

response = send_request('signup', 'POST', {'email':'john_doe@gmail.com', 'password':'password'})
response.json()

# # Login

response = send_request('login', 'POST', {'email':'john_doe@gmail.com', 'password':'password'})
response = response.json()
token = response['token']
response

# # Send info

send_request('send_info', 'POST', {'favorite_color':'yello', 'favorite_fruit':'banana'},
             headers={'Authorization': f'Bearer {token}'})

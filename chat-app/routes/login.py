import requests

def login(username, password):
  response = requests.post('http://localhost:5000/login', json={
    'username': username,
    'password': password
  })
  if response.status_code == 200:
    token = response.json()['token']
    headers = {
      'Authorization': 'Bearer ' + token
    }
    return headers
  else:
    raise Exception('Failed to log in')

token = login('admin', 'password')

# Use the token to authenticate subsequent requests
response = requests.get('http://localhost:5000/rooms', headers=token)

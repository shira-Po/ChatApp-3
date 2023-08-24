import requests

def logout(token):
  response = requests.post('http://localhost:5000/logout', headers={
    'Authorization': 'Bearer ' + token
  })
  if response.status_code == 200:
    return True
  else:
    return False


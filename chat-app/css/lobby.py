import requests

def get_rooms(token):
  response = requests.get('http://localhost:5000/rooms', headers={
    'Authorization': 'Bearer ' + token
  })
  if response.status_code == 200:
    return response.json()
  else:
    return []

def create_room(token, room_name):
  response = requests.post('http://localhost:5000/rooms', json={
    'room_name': room_name
  }, headers={
    'Authorization': 'Bearer ' + token
  })
  if response.status_code == 200:
    return True
  else:
    return False

def join_room(token, room_name):
  response = requests.post('http://localhost:5000/rooms/' + room_name, headers={
    'Authorization': 'Bearer ' + token
  })
  if response.status_code == 200:
    return True
  else:
    return False

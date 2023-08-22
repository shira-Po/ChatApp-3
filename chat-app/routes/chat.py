import requests

def send_message(token, room_name, message):
  response = requests.post('http://localhost:5000/rooms/' + room_name + '/messages', json={
    'message': message
  }, headers={
    'Authorization': 'Bearer ' + token
  })
  if response.status_code == 200:
    return True
  else:
    return False

def get_messages(token, room_name):
  response = requests.get('http://localhost:5000/rooms/' + room_name + '/messages', headers={
    'Authorization': 'Bearer ' + token
  })
  if response.status_code == 200:
    return response.json()
  else:
    return []

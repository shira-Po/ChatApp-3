import datetime
from flask import Flask, render_template, request, redirect, session, jsonify
import csv
import os
import base64

app = Flask(__name__)

app.secret_key="secret_key"

room_files_path = os.getenv('ROOM_FILES_PATH')

#region helper functions

#used in register and in login functions
def check_user_registration(username, password,callFunction):
    with open('users.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        if callFunction=="login":
          for row in reader:
              if row[0] == username and decode_password(row[1]) == password:
                  return True
        elif callFunction=="register":
           for row in reader:
              if row[0] == username:
                  return True
    return False
  
def encode_password(password):
    encoded_bytes = base64.b64encode(password.encode('utf-8'))
    return encoded_bytes.decode('utf-8')



def decode_password(encoded_password):
    decoded_bytes = base64.b64decode(encoded_password.encode('utf-8'))
    return decoded_bytes.decode('utf-8')
#endregion

#region register
@app.route('/', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']
        encoded_pass=encode_password(userpass)
        
        #Check if the user already exists
        if check_user_registration(username, userpass,"register"):
          return redirect("/login")

        # Open the CSV file in read mode
        with open('users.csv', 'a',newline='') as file:
          writer=csv.writer(file)
          writer.writerow([username,encoded_pass])
        return redirect("/login")
        
    return render_template("register.html")
  
#endregion
  
#region login
@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']
        if check_user_registration(username,userpass,"login"):
            session['username'] = username
            return redirect('/lobby')
        else:
            return "Invalid credentials"
   return render_template('login.html')
#endregion

#region lobby
@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    if 'username' in session:
        if request.method == 'POST':
            room_name = request.form['new_room']
            try:
                with open(f'rooms/{room_name}.txt', 'x') as f:
                    f.write('Welcome! \n')
            except FileNotFoundError:
                print("The given room name already exists")
            print("CREATED NEW ROOM NAMED: " + room_name )
        rooms = os.listdir('rooms/')
        new_rooms = [x[:-4] for x in rooms]
        return render_template('lobby.html', rooms=new_rooms)  
    else:
        return redirect('/login')

#endregion

#region logout
@app.route("/logout")
def logout():
  session.pop('username', None)
  return redirect("/login")
#endregion

#region chat ( This function handles the chat page)
@app.route('/chat/<room>', methods=['GET', 'POST'])
def chat(room):
  if 'username' in session:
    if request.method == 'POST':
        return render_template('chat.html', room=room, messages=get_messages(room))
    else:
      messages = get_messages(room)
      return render_template('chat.html', room=room, messages=messages)
  else:
    return redirect('/login')

#endregion

#region update_content (This function handles the API for getting chat message)
@app.route('/api/chat/<room>', methods=["GET","POST"])
def get_messages(room):
  if request.method == "POST":
     f_path = "rooms/{}.txt".format(room)
     msg = request.form['msg']
     username = session['username']
     date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     with open(f_path, 'a') as f:
        f.write(f'[{date}] {username}: {msg}\n')
  else:
     with open(f_path, 'r') as f:
      f.seek(0)
      chat_messages = f.read()
      return chat_messages
#endregion
    



if __name__ == '__main__':
  app.run(host="0.0.0.0",debug=True)
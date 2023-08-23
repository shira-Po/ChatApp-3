from flask import Flask, render_template, request, redirect, session, jsonify
import csv
import base64

app = Flask(__name__)

# @app.route('/')
# def homePage():
#   return render_template("register.html")
  

# if __name__ == '__main__':
#   app.run(host="0.0.0.0",debug=True)
  


def encode_password(password):
    encoded_bytes = base64.b64encode(password.encode('utf-8'))
    return encoded_bytes.decode('utf-8')



def decode_password(encoded_password):
    decoded_bytes = base64.b64decode(encoded_password.encode('utf-8'))
    return decoded_bytes.decode('utf-8')


def check_user_registration(username, password):
    with open('users.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and decode_password(row[1]) == password:
                return True
    return False



@app.route('/', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']
        encoded_pass=encode_password(userpass)
        
        #Check if the user already exists
        if check_user_registration(username, userpass):
          return redirect("/login")

        # Open the CSV file in read mode
        with open('users.csv', 'a',newline='') as file:
          writer=csv.writer(file)
          writer.writerow([username,encoded_pass])
        return redirect("/login")
        
    return render_template("register.html")
  
  


@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']
        if check_user_registration(username,userpass):
            session['username'] = username
            return redirect('/lobby')
        else:
            return "Invalid credentials. Please try again."
   return render_template('login.html')


@app.route("/lobby")
def lobby():
  if not session.get("username"):
    return redirect("/login")
  return render_template("lobby.html")

@app.route("/logout")
def logout():
  session.clear()
  return redirect("/login")




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  
  
  
  
  
if __name__ == '__main__':
  app.run(host="0.0.0.0",debug=True)
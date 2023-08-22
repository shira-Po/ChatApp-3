from flask import Flask, render_template, redirect, request

from .routes import login

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    token = login(username, password)
    return redirect('/chat', headers={'Authorization': 'Bearer ' + token})
  else:
    return render_template('login.html')

@app.route('/chat')
def chatPage():
  return 'Hello, world!'

if __name__ == '__main__':
  app.run(debug=True)

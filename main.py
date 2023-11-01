from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b8c555d1b70c36d11c3793ec9949bd2bbf9add984e65b77a7b34d3ec7d9c2d28'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def hello_world():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('user_joined', {'username': username}, room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('user_left', {'username': username}, room=room)

@socketio.on('send_message')
def send_message(data):
    room = data['room']
    message = data['message']
    username = data['username']
    emit('receive_message', {'username': username, 'message': message}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
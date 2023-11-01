import pika
import os
from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
socketio = SocketIO(app, cors_allowed_origins="*")

url = os.environ.get('CLOUDAMQP_URL', '')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='chat_messages')

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

    # Publicar el mensaje en RabbitMQ
    channel.basic_publish(exchange='',
                          routing_key='chat_messages',
                          body=f"{room}|{username}|{message}")

    # Emitir el mensaje a través de SocketIO (esto se puede hacer desde un consumidor de RabbitMQ)
    emit('receive_message', {'username': username, 'message': message}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')


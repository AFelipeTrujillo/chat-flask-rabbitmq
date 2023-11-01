import pika
import os

def callback(ch, method, properties, body):
    room, username, message = body.decode().split('|')
    print(room, username, message)
    # Aquí, puedes emitir el mensaje a través de SocketIO
    # Por ejemplo: socketio.emit('receive_message', {'username': username, 'message': message}, room=room)

url = os.environ.get('CLOUDAMQP_URL', '')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='chat_messages')

channel.basic_consume('chat_messages', callback)
print(' [*] Waiting for messages:')
channel.start_consuming()
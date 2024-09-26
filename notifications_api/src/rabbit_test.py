import pika

# Подключение к RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        'localhost',
        5672,
        '/',
        pika.PlainCredentials('rabbit', 'rabbit'),
    )
)
channel = connection.channel()

# Создание очереди
channel.queue_declare(queue='hello')

# Публикация сообщения
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

# Закрытие соединения
connection.close()

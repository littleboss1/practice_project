#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('eternity_prod','xxxxxxx')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.99.70',5672,'/eternity_prod',credentials))
channel = connection.channel()

#declare
channel.queue_declare(queue='balance')

def callback(ch,method,properties,body):
    print(" [x] Receiver %r" % body)


channel.basic_consume(queue='balance',on_message_callback=callback,auto_ack=True)
print(" [*] Waiting for messages. To exit press CTRT+C")
try:
    channel.start_consuming()
except KeyboardInterrupt as e:
    print('exit')

#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('eternity_prod','xxxxxxx')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.99.70',5672,'/eternity_prod',credentials))
channel = connection.channel()

#declare
channel.queue_declare(queue='balance')
channel.basic_publish(exchange='',routing_key='balance',body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()

import pika


class RabbitMQ(object):
    def __init__(self, addr, rabbitMqName):
        self.mqAddr = addr
        self.msgQueueName = rabbitMqName

    def msg_on_recv(self, ch, mothod, properties, msg):
        print("[Consumer] recv %s" % msg)

    def msg_start(self):
        print("[Consumer] waiting for msg")

        self.mqParam = pika.ConnectionParameters(self.mqAddr)

        try:
            self.connection = pika.BlockingConnection(self.mqParam)

            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.msgQueueName)
            self.channel.basic_consume(self.msgQueueName, self.msg_on_recv)

            self.channel.start_consuming()
        except pika.exceptions.AMQPError as e:
            print('AMQPError {0} , {1}'.format(self.mqAddr, e))

    def msg_send(self, msg):
        print("[Producer] send %s" % msg)
        self.mqParam = pika.ConnectionParameters(self.mqAddr)

        try:
            self.connection = pika.BlockingConnection(self.mqParam)

            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.msgQueueName)

            self.channel.basic_publish(exchange='', routing_key=self.msgQueueName, body=msg)
        except pika.exceptions.AMQPError as e:
            print('AMQPError {0} , {1}'.format(self.mqAddr, e))

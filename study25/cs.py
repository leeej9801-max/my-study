from kafka import KafkaConsumer

cs = KafkaConsumer('test',bootstrap_servers=['localhost:9092'])

for msg in cs:
  print(msg.value)
from kafka import KafkaProducer

pd = KafkaProducer(bootstrap_servers='localhost:9092')

pd.send('test2', b'Hello3')
pd.flush()
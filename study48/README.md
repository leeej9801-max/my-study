## Spark 구성하기

- [Spark 다운로드](https://dlcdn.apache.org/spark/spark-4.1.1/spark-4.1.1-bin-hadoop3.tgz)
- Docker file 생성

```bash
FROM ubuntu:22.04
RUN apt-get update
RUN apt-get -y install wget openjdk-21-jdk

WORKDIR /opt/spark
RUN wget https://dlcdn.apache.org/spark/spark-4.1.1/spark-4.1.1-bin-hadoop3.tgz
RUN tar -zxvf spark-4.1.1-bin-hadoop3.tgz
RUN rm spark-4.1.1-bin-hadoop3.tgz

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-arm64
ENV SPARK_HOME=/opt/spark/spark-4.1.1-bin-hadoop3
ENV PATH="$PATH:${SPARK_HOME}/bin"
```

- Docker container 생성

```bash
docker run -d -it -p 8080:8080 -p 7077:7077 -e SPARK_PUBLIC=localhost --name master my-spark:latest
```

- Master 실행

```bash
start-master.sh
```

## pyspark 실행

```bash
uv init .
uv add pyspark
```

- python 파일 정의

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder
  .appName("PySpark WordCount Test")
  .master("spark://localhost:7077")
  .getOrCreate()
```
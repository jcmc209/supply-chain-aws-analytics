# Dockerfile para Hive Metastore con driver PostgreSQL y soporte S3A
FROM apache/hive:4.0.0

USER root

# Versiones de Hadoop y AWS SDK compatibles
ENV HADOOP_VERSION=3.3.4
ENV AWS_SDK_VERSION=1.12.262

# Instalar wget y descargar dependencias
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget && \
    # Driver PostgreSQL JDBC
    wget -q https://jdbc.postgresql.org/download/postgresql-42.6.0.jar \
        -O /opt/hive/lib/postgresql-42.6.0.jar && \
    # Hadoop AWS (S3A FileSystem)
    wget -q https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar \
        -O /opt/hive/lib/hadoop-aws-${HADOOP_VERSION}.jar && \
    # AWS SDK Bundle
    wget -q https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_VERSION}/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar \
        -O /opt/hive/lib/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER hive

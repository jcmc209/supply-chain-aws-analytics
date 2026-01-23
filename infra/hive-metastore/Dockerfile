FROM apache/hive:4.0.0

# PostgreSQL JDBC driver (sin curl, sin apt, sin yum)
ADD https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.4/postgresql-42.7.4.jar /opt/hive/lib/

# Por si acaso: permisos correctos
RUN chmod 644 /opt/hive/lib/postgresql-42.7.4.jar

FROM apache/hive:4.0.0

# Creamos carpeta propia writable para drivers
USER root
RUN mkdir -p /opt/hive/extra-jars

# PostgreSQL JDBC Driver (NO usamos curl/yum)
ADD https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.4/postgresql-42.7.4.jar /opt/hive/extra-jars/

# Asegurar lectura (si el filesystem deja)
RUN chmod 644 /opt/hive/extra-jars/postgresql-42.7.4.jar || true

# Hive carga jars adicionales desde HIVE_AUX_JARS_PATH
ENV HIVE_AUX_JARS_PATH=/opt/hive/extra-jars

USER hive

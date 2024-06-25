FROM postgres:13

ENV POSTGRES_DB=mydb
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password

COPY data/database.dump /tmp/

COPY init-db.sh /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh
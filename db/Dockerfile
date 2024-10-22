# pull official base image
FROM postgres:13

RUN apt-get update \
    && apt-get -y install net-tools netcat-traditional gcc tzdata \
    && apt-get clean

RUN locale-gen
ENV LANG C.UTF-8
ENV TZ Africa/Nairobi
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# run create.sql on init
ADD create.sql /docker-entrypoint-initdb.d
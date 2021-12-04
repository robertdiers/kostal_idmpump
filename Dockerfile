FROM debian:stable-slim

RUN apt update
RUN apt -y upgrade
RUN apt -y install cron python3 python3-pip
RUN pip3 install configparser pymodbus graphyte

# copy files
COPY kostal_idm.py /app/kostal_idm.py
COPY kostal_idm.ini /app/kostal_idm.ini
COPY kostal_idm.sh /app/kostal_idm.sh
COPY entrypoint.sh /app/entrypoint.sh
COPY container_cron /etc/cron.d/container_cron

# set workdir
WORKDIR /app

# give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/container_cron

# apply cron job
RUN crontab /etc/cron.d/container_cron

# run the command on container startup
CMD ["bash", "entrypoint.sh"]

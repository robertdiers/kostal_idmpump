FROM debian:stable-slim

RUN apt update
RUN apt -y upgrade
RUN apt -y install cron python3 python3-pip
RUN pip3 install pymodbus

# copy files
COPY kostal_idm.py /app/kostal_idm.py
COPY kostal_idm_cron /etc/cron.d/kostal_idm_cron

# set workdir
WORKDIR /app

# give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/kostal_idm_cron

# apply cron job
RUN crontab /etc/cron.d/kostal_idm_cron

# run the command on container startup
CMD ["cron", "-f"]

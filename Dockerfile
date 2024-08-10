FROM docker.io/debian:stable-slim

RUN apt update
RUN apt -y upgrade
RUN apt -y install cron python3 python3-dev python3-venv
RUN python3 -m venv ~/.local --system-site-packages
RUN ~/.local/bin/pip install configparser
RUN ~/.local/bin/pip install pymodbus
RUN ~/.local/bin/pip install pyserial_asyncio
RUN ~/.local/bin/pip install pyserial

RUN which python3

# copy files
COPY python /app/python
COPY shell/kostal-idm.sh /app/kostal-idm.sh
COPY shell/entrypoint.sh /app/entrypoint.sh
COPY shell/container_cron /etc/cron.d/container_cron

# set workdir
WORKDIR /app

# give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/container_cron

# apply cron job
RUN crontab /etc/cron.d/container_cron

# run the command on container startup
CMD ["bash", "entrypoint.sh"]

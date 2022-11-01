printenv | grep -v "no_proxy" >> /etc/environment
echo 'starting cron'
cd /app
cron -f
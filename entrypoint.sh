printenv | grep -v "no_proxy" >> /etc/environment
echo 'environment stored'
cron -f
echo 'cron initialized'
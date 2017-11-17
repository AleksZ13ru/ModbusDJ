source Mod*/bin/activate

cd Py*/Mod*

celery -A ModbusDJ worker -l info --concurrency=1 # terminal 1

celery -A ModbusDJ beat -l info --scheduler django_celery_beat.schedulers.DatabaseScheduler  # terminal 2

todo:
add calendar in form:list, detail
visual history data in select calendar data
modify function show in javascript, disable use old version REST function("mb_json2_time_stamp_detail"), use new function  "json_tstamp_detail"
clear comment string old code
add project to github


todo:start in raspberry pi 3
1. create virtualenv
2. install pakets: pip install -r requirements.txt
3. setting postgresql:
3.1. test run: sudo -u postgres psql
CREATE DATABASE db;
CREATE USER postuser WITH password 'passuser';
GRANT ALL ON DATABASE db TO postuser;

3.2. migrate date from db
old server: ./manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json

new server: ./manage.py loaddata db.json

3.3 setting celery broker: rabbitmq

sudo apt-get install rabbitmq-server
sudo rabbitmqctl add_user celeryuser celerypass
sudo rabbitmqctl add_vhost myvhost
sudo rabbitmqctl set_user_tags celeryuser mytag
sudo rabbitmqctl set_permissions -p myvhost celeryuser ".*" ".*" ".*"

CELERY_BROKER_URL = 'amqp://celeryuser:celerypass@localhost:5672/myvhost'

4. add start celery and django in sustemd

todo: run from raspberry pi3
ssh pi@192.168.1.241
source venv/M*/bin/activate
cd Mod*
python manage.py 0.0.0.0:8000

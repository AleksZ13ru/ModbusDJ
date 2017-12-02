source Mod*/bin/activate

git clone https://github.com/AleksZ13ru/ModbusDJ.git

cd Py*/Mod*

celery -A ModbusDJ worker -l info --concurrency=1 # terminal 1

celery -A ModbusDJ beat -l info --scheduler django_celery_beat.schedulers.DatabaseScheduler  # terminal 2

todo:
+ add calendar in form:list, detail
visual history data in select calendar data
modify function show in javascript, disable use old version REST function("mb_json2_time_stamp_detail"), use new function  "json_tstamp_detail"
+ clear comment string old code
+ add project to github


todo:start in raspberry pi 3
0.  wget https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py
    install virtualenv: pip3 install virtualenv
1. sudo apt-get install git, python3-dev
2.0. create virtualenv: virtualenv ModbusVEN
2.1. git clone https://github.com/AleksZ13ru/ModbusDJ.git
2.2. install pakets: pip install -r requirements.txt - !I am have problem to install from file, single install OK

3. setting postgresql:
3.0. install:
    sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
    wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
    sudo apt-get update
    sudo apt-get install postgresql postgresql-contrib
3.1. test run: sudo -u postgres psql
CREATE DATABASE db;
CREATE USER postuser WITH password 'passuser';
GRANT ALL ON DATABASE db TO postuser;
\q
3.2. migrate date from db
python manage.py migrate
old server: ./manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json

new server: python manage.py loaddata db.json

3.3 setting celery broker: rabbitmq

sudo apt-get install rabbitmq-server
sudo rabbitmqctl add_user celeryuser celerypass
sudo rabbitmqctl add_vhost myvhost
sudo rabbitmqctl set_user_tags celeryuser mytag
sudo rabbitmqctl set_permissions -p myvhost celeryuser ".*" ".*" ".*"

CELERY_BROKER_URL = 'amqp://celeryuser:celerypass@localhost:5672/myvhost'

4. add start celery and django in sustemd
5. sudo apt-get install nginx

5.1 setting nginx in file: sudo nano /etc/nginx/sites-available/default :
	server {
    		listen 80;
    		server_name 0.0.0.0;
    		access_log  /var/log/nginx/example.log;

    		location /static/ {
        		root /home/pi/ModbusDJ/;
        		expires 30d;
    		}

    		location / {
        		proxy_pass http://127.0.0.1:8000;
        		proxy_set_header Host $server_name;
        		proxy_set_header X-Real-IP $remote_addr;
        		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    		}
  	}

sudo service nginx restart
5.2.1. add line to file setting project:
	STATIC_URL = '/static/'
	STATIC_ROOT = os.path.join(BASE_DIR, 'static')
5.2.2.python manage.py collectstatic

6. add file configuration start gunicorn, celery_w, celery_b
6.1.

ModbusDJ.service
-------------------------------------
[Unit]
Description=Unit for starting a basic Django app
After=multi-user.target

[Service]
Restart=always
RestartSec=10
Type=idle
WorkingDirectory=/home/pi/ModbusDJ
ExecStart=/home/pi/ModbusVEN/bin/gunicorn ModbusDJ.wsgi:application --bind 127.0.0.1:8000 -t 120 -w 2

[Install]
WantedBy=multi-user.target
-------------------------------------

CeleryW
-------------------------------------
[Unit]
Description=CeleryW Django app
After=multi-user.target

[Service]
Restart=always
RestartSec=10
Type=idle
WorkingDirectory=/home/pi/ModbusDJ
ExecStart=/home/pi/ModbusVEN/bin/celery -A ModbusDJ worker -l info --concurrency=1

[Install]
WantedBy=multi-user.target
-------------------------------------

CeleryB
-------------------------------------
[Unit]
Description=CeleryB Django app
After=multi-user.target

[Service]
Restart=always
RestartSec=10
Type=idle
WorkingDirectory=/home/pi/ModbusDJ
ExecStart=/home/pi/ModbusVEN/bin/celery -A ModbusDJ beat -l info --scheduler django_celery_beat.schedulers.DatabaseScheduler

[Install]
WantedBy=multi-user.target
-------------------------------------

6.2.
    sudo systemctl status ModbusDJ
    sudo systemctl enable ModbusDJ
    sudo systemctl -l status ModbusDJ

todo: run from raspberry pi3
ssh pi@192.168.1.241
source venv/M*/bin/activate
cd Mod*
python manage.py 0.0.0.0:8000

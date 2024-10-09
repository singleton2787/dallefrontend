bind = "0.0.0.0:8000"
workers = 3
wsgi_app = "dalle.wsgi:application"
[Unit]
Description=Gunicorn daemon for DALL-E project
After=network.target

[Service]
User=malibu
Group=www-data
WorkingDirectory=/home/malibu/dalle_project
ExecStart=/home/malibu/dalle_project/venv/bin/python /home/malibu/dalle_project/venv/bin/gunicorn --bind 0.0.0.0:8000 dalle.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
#Required packages:

*nginx
*python3.6 // sudo add-apt-repository ppa:fkrull/deadsnakes
*virtualenv + pip
*git

sudo apt-get install nginx git python3.6 python3.6-venv

#Nginx Virtual Host config
*nginx.template.conf
*edit SITENAME

#Systemd service
*gunicorn-systemd.template.service
*edit SITENAME

#Folder structure

/home/username
└── sites
    ├── SITENAME
        ├── database
        ├── source
        ├── static
        └── virtualenv

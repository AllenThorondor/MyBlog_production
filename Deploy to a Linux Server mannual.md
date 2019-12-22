# Deployment SOP(standard operation procedure)



## Part1: Server Initialization

1. Login server use ssh root@IP_address

2. Update software conditions using: apt update && apt upgrade

3. Set hostname for machine:

   1. hostnamectl set-hostname flask-server
   2. vi /etc/hosts
   3. 47.106.21.181 flask-server
   4. adduser Leonard
   5. adduser Leonard sudo (add this person to sudo group )
   6. exit (to login as Leonard, you have to exit first)
   7. re-login as Leonard

4. Set secretly based login

   1. Pwd  to know where you are

   2. make ssh key based authentication instead of login by password

   3. on server $: mkdir .ssh

      1. on local machine: ssh-keygen -b 4096
      2. copy the public key to server:    scp ~/.ssh/id_rsa.pub leonard@47.106.21.181:~/.ssh/authorized_keys

   4. on server : ls .ssh

      1. you can see the authorised_keys on the console 
      2. change the mode of ssh file.   :     sudo chmod 700 ~/.ssh/
      3. Change the mode of all the files in the ssh.   : sudo chmod 600 ~/.ssh/*
      4. and then you exit and re log in , you will find you need not enter the password because you are using the public key right now .
      5. sudo vi /etc/ssh/sshd_config
         1. passwordAuthentication : no
         2. PermitRootLogin:  no
      6. Restart the server :   sudo systemctl restart ssh

      

      

## Part2: Setup Firewall

1. (setup the firewall )sudo apt install ufw ( get the uncomplicated simple firewall )
   1. sudo ufw default allow outgoing
   2. sudo ufw default deny incoming
   3. sudo ufw allow ssh
   4. sudo ufw allow 5000 (this is to allow port 5000)
   5. sudo ufw enable. (to neable all the settings just set)ex
   6. sudo ufw status



## Part3: File transfer to server

1. On the local machine:

   1. pip freeze > requirements.txt
   2. (to copy all the project file to server)  
   3. scp -r python/python3/Clone_repo/Flask_Blog leonard@183.239.147.178:~/

2. On the server side:

   1. (Create a virtual env on the server first)

      1. sudo apt install python3-pip
      2. sudo apt install python3-venv (or use another command :  sudo apt-get install python3-venv)
      3. pip freeze > requirement.txt    (preparation to auto pip install packages that we need)
      4. pip install -r requirement.txt 

   2. Environment variables (config file instead)

      1. sudo vi flaskblog/config.py 
      2. export FLASK_APP=run.py
      3. flask run --host=0.0.0.0

   3. install nginx for web:

      1. sudo apt install nginx
      2. pip install gunicorn

   4. update config for nginx

      1. gunicorn will handle the python code , and nginx will handle th static files

      2. first remove default file: (  sudo rm /etc/nginx/sites-enabled/default ) 

      3. create new config : (  sudo vi /etc/nginx/sites-enabled/flaskblog  )

      4. server {

         ​    listen 80;

         ​    server_name 111.229.109.128;

         

         ​    location /static {

         ​        alias /home/leonard/Flask_Blog/flaskblog/static;

         ​    }

         

         ​    location / {

         ​        proxy_pass http://localhost:8000;

         ​        include /etc/nginx/proxy_params;

         ​        proxy_redirect off;

         

         

         ​    }

         }

      5. sudo ufw allow http/tcp

      6. sudo ufw delete allow 5000

      7. sudo ufw enable

      8. sudo systemctl restart nginx

   5. gunicore config set up:

      1. gunicorn -w 3 run:app (now you can visit your web site, and this is not enough cause once you close your server, everything gone)

      2. sudo apt install supervisor ( help you manager your web server )

      3. sudo vi /etc/supervisor/conf.d/flaskblog.conf

      4. [program:flaskblog]

         directory=/home/leonard/Flask_Blog

         command=/home/leonard/Flask_Blog/venv/bin/gunicorn -w 3 run:app

         user=leonard

         autostart=true

         autorestart=true

         stopasgroup=true

         killasgroup=true

         stderr_logfile=/var/log/flaskblog/flaskblog.err.log

         stdout_logfile=/var/log/flaskblog/flaskblog.out.log

      5. sudo mkdir -p /var/log/flaskblog

      6. sudo touch /var/log/flaskblog/flaskblog.out.log

      7. sudo touch /var/log/flaskblog/flaskblog.err.log

      8. sudo supervisorctl reload ( to restart the supervisor )

   6. to change the size limit for nginx for image files (2MB for default)

      1. sudo vi /etc/nginx/nginx.conf
      2. add 1 line above the token off ( client_max_body_size 5M; )
      3. restart nginx ( sudo systemctl restart nginx )
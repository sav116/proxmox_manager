#/bin/bash
set -xe

git reset --hard origin/master
git pull
pip3.11 install -r requirements.txt

cp remote_controller.service /etc/systemd/system
systemctl daemon-reload
systemctl restart remote_controller
systemctl status remote_controller
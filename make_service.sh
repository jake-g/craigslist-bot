echo "must have > python3.6"
python3 -V

pip3 install -r requirements.txt

cat << _EOF_ > /etc/systemd/system/craig-bot.service
[Unit]
Description=craig-bot system service
After=graphical.target

[Service]
User=root
Group=dietpi
Type=simple
ExecStart=/usr/bin/python3 -u /root/craig-bot/main_loop.py

[Install]
WantedBy=default.target
_EOF_

systemctl enable craig-bot.service
systemctl daemon-reload

echo "alias criag-bot='journalctl --unit=craig-bot -n 10 -f --no-pager'" >> ~/.bashrc



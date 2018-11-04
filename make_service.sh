
# first arg should be service name 
# and have a corresponding settings-[service-name].py
name=$1
if [ $# -eq 0 ]
  then
    echo "Error pass in service name"
    exit 1
fi
settings="settings-""$name"".py"
echo "Making service: ""$name"

NAME="craigslist-""$name"
DIR="deployment/services/""$NAME"/
mkdir -p "$DIR"
echo "Service folder: ""$DIR"

# copy src files
cp "$settings" "$DIR""settings.py"
declare -a copy=("util.py" "scraper.py" "requirements.txt" "main_loop.py")
for i in "${copy[@]}"
do
   cp "$i" "$DIR""$i"
done


# service file
echo "[Unit]
Description=Run craigslist bot

[Service]
User=root
Group=dietpi
Type=simple
ExecStart=/usr/bin/python3 -u /opt/"$NAME"/main_loop.py

WorkingDirectory=/opt/"$NAME"/
Environment=SLACK_TOKEN=xoxp-139047967344-139832954196-153246389329-865763cff4c1680419bcfd1a9005dac1
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target" > "$DIR""$NAME"".service"

# install script steps
echo "sudo apt-get install -y python3" > "$DIR""install.sh"
echo "pip3 install setuptools" >> "$DIR""install.sh"
echo "pip3 install -r requirements.txt" >> "$DIR""install.sh"
echo "mkdir /opt/"$NAME"" >> "$DIR""install.sh"
echo "cp -r * /opt/"$NAME"" >> "$DIR""install.sh"
echo "cp "$NAME"".service" /lib/systemd/system/" >> "$DIR""install.sh"

# uninstall script steps
echo "sudo rm -rf /opt/"$NAME"" >> "$DIR""uninstall.sh"
echo "sudo rm /lib/systemd/system/"$NAME"".service"" >> "$DIR""uninstall.sh"


echo
echo "Now you need to activate the service..."
echo "Can add to : /DietPi/dietpi/.dietpi-services_include_exclude"
echo "Can also start with: systemctl daemon-reload && systemctl enable "$NAME" && systemctl start "$NAME" --no-block"
echo "View logs: systemctl status "$NAME""
echo "Stream log with: journalctl --unit="$NAME" -n 100 --no-pager"


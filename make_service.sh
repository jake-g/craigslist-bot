
# first arg should be service name 
# and have a corresponding settings-[service-name].py
name=$1
if [ $# -eq 0 ]
  then
    echo "Error pass in service name"
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
ExecStart=/usr/bin/python3 /opt/"$NAME"/main.py
WorkingDirectory=/opt/"$NAME"/
Environment=SLACK_TOKEN=xoxp-139047967344-139832954196-153246389329-865763cff4c1680419bcfd1a9005dac1
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target" > "$DIR""$NAME"".service"

# install script steps
echo "sudo apt-get install -y python3" > "$DIR""setup.sh"
echo "pip install -r requirements.txt" >> "$DIR""setup.sh"
echo "mkdir /opt/"$NAME"" >> "$DIR""setup.sh"
echo "cp -r * /opt/"$NAME"" >> "$DIR""setup.sh"
echo "cp "$NAME"".service" /lib/systemd/system/" >> "$DIR""setup.sh"



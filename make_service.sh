
name="music-gear"
settings="settings-""$name"".py"
echo "Making service: ""$name"
DIR="deployment/services/craigslist-""$name""/"
mkdir -p "$DIR"
echo "Service folder: ""$DIR"

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
ExecStart=/usr/bin/python3 /opt/"$DIR"main.py
WorkingDirectory=/opt/"$DIR"
Environment=SLACK_TOKEN=xoxp-139047967344-139832954196-153246389329-865763cff4c1680419bcfd1a9005dac1
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target" > "$DIR""craigslist-""$name"".service"

# install script steps
echo "sudo apt-get install -y python3" > "$DIR""setup.sh"
echo "pip install -r requirements.txt" >> "$DIR""setup.sh"
echo "mkdir /opt/"$DIR"" >> "$DIR""setup.sh"
echo "cp -r * /opt/"$DIR"" >> "$DIR""setup.sh"
echo "cp "craigslist-""$name"".service" /lib/systemd/system/" >> "$DIR""setup.sh"



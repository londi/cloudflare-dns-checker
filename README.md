# Cloudflare DNS Checker

### TL;DR;

This python tool helps you to keep the A-Record of your DNS zone up to date. The only thing you have to do is to schedule this script with a cronjob or similar. Have fun! ;-)

![Discord bot message](images/discord_bot_msg.png)

## How it work's

1. Get the current WAN ip address
2. Login to the cloudflare api and get the ip address of the first a-record
3. Change it if it's necessary
4. send a discord message about the ip state (if it has changed or not)

### Open Tasks

- Implement several Null-Checks
- Add error msgs
- Logger

## Install

1. Clone the repo to your system

```shell
git clone https://github.com/londi/cloudflare-dns-checker.git
```

2. Credentials

Add your credentials and information at the top in the main.py file

3. Install the requirements

```shell
pip3 install -r requirements.txt
```

4. Start the program

```shell
python3 main.py
```

## Run with crontab

Here is an example how you could run the program as a cronjob every noon and midnight.

```shell
0 0,12 * * * /usr/bin/python3 /root/dns-checker/cloudflare-dns-checker/main.py
```

More precisely it means: "At minute 0 past hour 0 and 12.".

Hint: I recommend the following website to easy create time schedule expressions: [crontab.guru](https://crontab.guru/)

To check where python3 is installed, use the "which" command:
```shell
which python3
/usr/bin/python3
```

Also helpful... check which timezone is set on your system (e.g. ubuntu):
```shell
# get current datetime
date

# set timezone
tzselect

# set permanent
nano ~/.profile
TZ='Europe/Zurich'; export TZ
```

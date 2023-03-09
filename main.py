import CloudFlare
from requests import get
import requests

# Cloudflare vars
EMAIL = '' # Your cloudflare email address
KEY = '' # Your global API Key: https://dash.cloudflare.com/profile/api-tokens
ZONE_NAME = '' # i.e. your website name
CLOUDFLARE_DNS_LINK = '' # is only used for your discord message to let you quickly open your dns settings if something went wront

# Discord vars
DISCORD_URL = '' # Webhook url of your discord channel

class CloudflareDnsChecker:

    def __init__(self):
        self.get_public_ip()
        self.check_and_set_dns_record()
        print(f'IP Changed: {self.ip_changed}, DNS Record updated: {self.dns_record_updated}')
        print('Send discord message')
        self.send_discord_message()


    def get_public_ip(self):
        ip = get('https://api.ipify.org').content.decode('utf8')
        print(f'Public IP address is: {ip}')
        self.public_ip = ip
        

    def check_and_set_dns_record(self):
        self.ip_changed = False
        self.dns_record_updated = False

        cf = CloudFlare.CloudFlare(email=EMAIL, key=KEY)

        # fetch zone
        zone_info = cf.zones.get(params={"name": ZONE_NAME})
        zone_id = zone_info[0]['id']
        print(f'Zone ID: {zone_id}')

        # fetch existing a record
        a_record = cf.zones.dns_records.get(zone_id, params={"name": ZONE_NAME, "type": "A"})[0]
        print(f'A Record: {a_record["content"]}')

        # check if ip changed
        if a_record["content"] != self.public_ip:
            self.ip_changed = True
            ## Update dns record
            a_record["content"] = self.public_ip
            cf.zones.dns_records.put(zone_id, a_record["id"], data=a_record)
            self.dns_record_updated = True
    

    def send_discord_message(self):
        headers = {'Content-Type': 'application/json'}
        discord_msg_ip_ok = {
            "content": "News from the DNS Checker",
            "embeds": [
                {
                "title": f"[OK] The IP Address is still the same :white_check_mark:",
                "description": f"Current IP: {self.public_ip}\nThe DNS Record is up to date.\n\n[Cloudflare DNS Records]({CLOUDFLARE_DNS_LINK})",
                "color": 5814783
                }
            ],
            "attachments": []
        }
        discord_msg_ip_changed = {
            "content": "News from the DNS Checker",
            "embeds": [
                {
                "title": f"[{'NOK' if self.ip_changed and not self.dns_record_updated else 'OK'}] The IP Address has changed :warning:",
                "description": f"New IP: {self.public_ip}\nThe DNS Record is up to date: {self.dns_record_updated}\n\n[Cloudflare DNS Records]({CLOUDFLARE_DNS_LINK})",
                "color": 5814783
                }
            ],
            "attachments": []
        }

        if self.ip_changed:
            discord_msg = discord_msg_ip_changed
        else:
            discord_msg = discord_msg_ip_ok

        r = requests.post(DISCORD_URL, 
                          json=discord_msg, headers=headers)
        print(f'Discord message send result: {r}')




if __name__ == '__main__':
    c = CloudflareDnsChecker()
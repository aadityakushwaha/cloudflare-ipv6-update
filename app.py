import os
import requests
import time
import logging

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Constants
ZONE_ID = os.getenv('ZONE_ID')
RECORD_ID = os.getenv('RECORD_ID')
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
CHECK_INTERVAL = 30  # Time between checks in seconds

# Cloudflare API endpoint
CLOUDFLARE_API_URL = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{RECORD_ID}"

# Headers for the Cloudflare API
HEADERS = {
    "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
    "Content-Type": "application/json"
}

def get_current_ipv6():
    response = requests.get('https://api64.ipify.org?format=json')
    response.raise_for_status()
    return response.json()['ip']

def get_cloudflare_ipv6():
    response = requests.get(CLOUDFLARE_API_URL, headers=HEADERS)
    response.raise_for_status()
    return response.json()['result']['content']

def update_cloudflare_ipv6(new_ip):
    data = {
        "type": "AAAA",
        "name": "altacee.com",
        "content": new_ip,
        "ttl": 120,  # Time to live
        "proxied": False  # Change to True if you want Cloudflare proxy enabled
    }
    response = requests.put(CLOUDFLARE_API_URL, headers=HEADERS, json=data)
    response.raise_for_status()
    return response.json()

def main():
    previous_ip = get_cloudflare_ipv6()

    while True:
        try:
            current_ip = get_current_ipv6()
            if current_ip != previous_ip:
                logging.info(f"IP change detected: {previous_ip} -> {current_ip}")
                update_response = update_cloudflare_ipv6(current_ip)
                if update_response['success']:
                    logging.info(f"Updated Cloudflare DNS to {current_ip}")
                    previous_ip = current_ip
                else:
                    logging.error(f"Failed to update Cloudflare DNS: {update_response}")
            else:
                logging.info(f"No IP change detected. Current IP: {current_ip}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()


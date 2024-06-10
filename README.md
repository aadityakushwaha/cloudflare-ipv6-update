A python script that updates ipv6 on Cloudflare every 30 seconds

**Note:** To get RULE_ID
```bash
curl -X GET 'https://api.cloudflare.com/client/v4/zones/<ZONE_ID>/dns_records' -H 'Authorization: Bearer API_TOKEN'
```

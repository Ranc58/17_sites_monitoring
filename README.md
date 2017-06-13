# Sites Monitoring Utility
This program check response of site and domain experation date.

# How to install:
1. Recomended use venv or virtualenv for better isolation.\
   Venv setup example: \
   `python3 -m venv myenv`\
   `source myenv/bin/activate`
2. Install requirements: \
   `pip3 install -r requirements.txt` (alternatively try add `sudo` before command)
3. Put list of URLs to file `sites.txt` in script folder. **URLs must be in each line one by one**!

# Launch example.
Use argument `-f` for pathway to file with URLs.

Run with default list `sites.txt` (it's in script folder for example)
```
$ python3 check_sites_health.py -f sites.txt

Url: https://google.com
Server response: 200
To end of domen expiration: 39 months

Url: https://devman.org
Server response: 200
To end of domen expiration: 2 months
```
# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

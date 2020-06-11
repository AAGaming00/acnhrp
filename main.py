import requests
from pypresence import Presence
from time import sleep
import json
import auth
import os
import sys
s = requests.session()


discorddiscord = Presence("720066058051911701", pipe=0, loop=None, handler=None)
if getattr(sys, 'frozen', False):
	app_path = os.path.dirname(sys.executable)
elif __file__:
	app_path = os.path.dirname(__file__)
config_path = os.path.join(app_path, "config.txt")
config_file = open(config_path, "r+")
config_data = json.load(config_file)

if config_data["session_token"] == "":
    loginsession = auth.log_in("1.0.0")
    config_data["session_token"] = loginsession
    config_file.seek(0)
    json.dump(config_data, config_file)
    config_file.truncate()
tokenn = auth.get_cookie(config_data["session_token"], "en-US", "1")

config_file.close()
print(tokenn)
cookies = '_dnt=0; _ga=GA1.2.557708532.1591733570; _gid=GA1.2.2125084658.1591733570; _gtoken=' + str(tokenn) + ";"
uheaders = {
'Host':	'web.sd.lp1.acbaa.srv.nintendo.net',
'Connection': 'keep-alive',
'Accept': 'application/json, text/plain, */*',
'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G965N Build/R16NW.G965NKSU1ARC7; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36',
'Referer': 'https://web.sd.lp1.acbaa.srv.nintendo.net/?lang=en-US&na_country=US&na_lang=en-US',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'en-US,en;q=0.9',
'Cookie': cookies,
'X-Requested-With': 'com.nintendo.znca',
'If-None-Match': 'W/"5437202285e1c9c40f9b04b2b0ded42b"'
}
print(s.cookies)
dis = None
usersurl = 'https://web.sd.lp1.acbaa.srv.nintendo.net/api/sd/v1/users'
user = s.get(usersurl, headers=uheaders)
print(user.text)
bearer = auth.get_bearer(tokenn, user.json()["users"][0]["id"])
url = 'https://web.sd.lp1.acbaa.srv.nintendo.net/api/sd/v1/messages'
data = '{"body": "😀","type": "keyboard"}'.encode('utf-8')

headers = {
   "Host": "web.sd.lp1.acbaa.srv.nintendo.net",
   "Connection": "keep-alive",
   "Content-Length": "33",
   "Accept": "application/json, text/plain, */*",
   "Origin": "https://web.sd.lp1.acbaa.srv.nintendo.net",
   "Authorization": "Bearer " + bearer,
   "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G965N Build/R16NW.G965NKSU1ARC7; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36",
   "Content-Type": "application/json",
   "Referer": "https://web.sd.lp1.acbaa.srv.nintendo.net/players/chat",
   "Accept-Encoding": "gzip, deflate",
   "Accept-Language": "en-US,en;q=0.9",
   "Cookie": cookies,
   "X-Requested-With": "com.nintendo.znca"
}

print(user)
while True:
    x = requests.post(url, data = data, headers = headers)

    if x.status_code == 403:
        print("you are offline")
        if dis:
            discorddiscord.close()
            dis = False
    if x.status_code == 201:
        print("you are online")
        if not dis:
            discorddiscord.connect()
            discorddiscord.update(state=user.json()["users"][0]["land"]["name"], details = user.json()["users"][0]["name"])
            dis = True
    print(x)
    sleep(10)

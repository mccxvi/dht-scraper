#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#/////////////////////////////////////////

# 🠺 21/02/2023 21:31:35
#
# ↳ Author 🡢 Mikołaj Połonowicz @ MCCXVI
# ↳ https://github.com/mccxvi

#/////////////////////////////////////////

from datetime import datetime
from urllib.parse import urljoin, urlparse
import os, re, requests, json

def SanatizeUsername(username):
	FORBIDDEN_CHARS = ["\\", "/", ":", "*", "?", "<", ">", "|"]
	SanitizedUser = username

	for i in FORBIDDEN_CHARS:
		SanitizedUser = SanitizedUser.replace(i,"")
		
	return SanitizedUser

if not os.path.exists(f'dl'):
    os.makedirs(f'dl')

serverFile = input(" * | DHT File location: ")

with open(serverFile, encoding="utf-8") as rd:
	data = json.load(rd)
	dbContent = data['data']
	chnContent = data['meta']['channels']
	findServerName = data['meta']['servers']
	usrIndex = data['meta']['users']

for i in findServerName:
	serverName = i['name']
	serverType = i['type']

if serverType == "DM":
	deliminatorType = "DIRECT MESSAGES"

if serverType == "SERVER":
	deliminatorType = "SERVER"

if serverType == "GROUP":
	deliminatorType = "GROUP CHAT"

if not os.path.exists(f'dl/{serverName}'):
    os.makedirs(f'dl/{serverName}')

userIndex = {}
channelsFriendlyName = {}

ind = 0
for i in usrIndex:
	userIndex[ind] = usrIndex[i]['name']
	ind += 1

for i in chnContent:
	channelsFriendlyName[f'{i}'] = (f'{chnContent[i]["name"]}')


for cid in dbContent:
	for (post, inside) in dbContent[cid].items():
		if "a" in inside:
			for cont in inside['a']:
				urlog = cont['url']
				url = urljoin(urlog, urlparse(urlog).path)

				response = requests.get(urlog)	
				orgfname = re.search("([a-zA-Z0-9\\s_\\.\\-\\(\\):])+$", url)[0]

				for fcn in channelsFriendlyName:
					if cid == fcn:
						properChannelName = channelsFriendlyName[fcn]

						if not os.path.exists(f'dl/{serverName}/{properChannelName}'):
						    os.makedirs(f'dl/{serverName}/{properChannelName}')

						for userid in userIndex:
							if inside['u'] == userid:
								IndexUsername = str(userIndex[userid])
								SanitizedUser = SanatizeUsername(IndexUsername)

						msgTimestamp = str(inside['t'])[:-3]
						fileTimestamp = datetime.fromtimestamp(int(msgTimestamp))
						FileTime = (fileTimestamp.strftime("%Y-%m-%d %H%M%S"))

						if response.status_code == 404:
							print(f" - | 404 (Not Found) '[{FileTime}] {SanitizedUser}_{orgfname}' from [{properChannelName}]")
						else:
							with open(f"dl/{serverName}/{properChannelName}/[{FileTime}] {SanitizedUser}_{orgfname}", "wb") as f:
								f.write(response.content)

							print(f" + | Downloaded '[{FileTime}] {SanitizedUser}_{orgfname}' from [{properChannelName}]")			
		else:
			pass

print(f"\n * | FINISHED DOWNLOADING FROM '{serverName}' {deliminatorType}")

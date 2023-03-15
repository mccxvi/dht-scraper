#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#/////////////////////////////////////////

# 🠺 21/02/2023 21:31:35
#
# ↳ Author 🡢 Mikołaj Połonowicz @ MCCXVI
# ↳ https://github.com/mccxvi

#/////////////////////////////////////////

import shutil
import os
import requests
import mimetypes
import json
import re
import secrets
from datetime import datetime

def SanatizeUsername(username):
	FORBIDDEN_CHARS = ["\", /", ":", "*", "?", "<", ">", "|"]

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
				url = cont['url']
				response = requests.get(url)
				content_type = response.headers['content-type']
				ext = mimetypes.guess_extension(content_type)
				if ext == None:
					print(f" - | File doesn't exist anymore [Skipping]")
				else:
					fname = secrets.token_urlsafe(12)

					for fcn in channelsFriendlyName:
						if cid == fcn:
							properChannelName = channelsFriendlyName[fcn]

							if not os.path.exists(f'dl/{serverName}/{properChannelName}'):
							    os.makedirs(f'dl/{serverName}/{properChannelName}')

							if not os.path.exists(f'dl/{serverName}/{properChannelName}/{ext}'):
								os.makedirs(f'dl/{serverName}/{properChannelName}/{ext}')

							for userid in userIndex:
								if inside['u'] == userid:
									IndexUsername = str(userIndex[userid])
									SanitizedUser = SanatizeUsername(IndexUsername)

							msgTimestamp = str(inside['t'])[:-3]
							fileTimestamp = datetime.fromtimestamp(int(msgTimestamp))
							FileTime = (fileTimestamp.strftime("%Y-%m-%d"))

							with open(f"dl/{serverName}/{properChannelName}/{ext}/[{FileTime}] {SanitizedUser}_{fname}{ext}", "wb") as f:
								f.write(response.content)

							print(f" + | Downloaded '[{FileTime}] {SanitizedUser}_{fname}{ext}' from [{properChannelName}]")			
		else:
			pass

print(f"\n * | FINISHED DOWNLOADING FROM '{serverName}' {deliminatorType}")
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

if not os.path.exists(f'dl'):
    os.makedirs(f'dl')

serverFile = input(" * | DHT File location: ")

with open(serverFile, encoding="utf-8") as rd:
	data = json.load(rd)
	dbContent = data['data']
	chnContent = data['meta']['channels']
	findServerName = data['meta']['servers']

for i in findServerName:
	serverName = i['name']

if not os.path.exists(f'dl/{serverName}'):
    os.makedirs(f'dl/{serverName}')

channelsFriendlyName = {}

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

							with open(f"dl/{serverName}/{properChannelName}/{ext}/{fname}{ext}", "wb") as f:
								f.write(response.content)

							print(f" + | Downloaded '{fname}{ext}' from [{properChannelName}]")			
		else:
			pass

print(f"\n * | FINISHED DOWNLOADING FROM '{serverName}' SERVER")
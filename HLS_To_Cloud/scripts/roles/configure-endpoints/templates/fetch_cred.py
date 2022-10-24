import os
from netrc import netrc
import requests as r
import json

nrc = '.netrc'
netrcDir = os.path.expanduser(f"~/{nrc}")
urs = 'urs.earthdata.nasa.gov'
netrc(netrcDir).authenticators(urs)[0]

resp = r.get("https://data.lpdaac.earthdatacloud.nasa.gov/s3credentials").json()

print(json.dumps(resp))
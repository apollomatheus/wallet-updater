#!/usr/bin/python
from decimal import *
from bitcoinrpc.authproxy import AuthServiceProxy
import json
import sys
import os
import requests

def runUpdate(v,l,d):
 os.system('./update.sh '+str(v)+' '+l+' '+d)

# Scheme
# {
#  "wallets": [
#   {
#     "id": "COIN",
#     "link": "http://...",
#     "version": 1000,
#     "daemon": "coind"
#   }
#  ]
# }
def apiArg():
 if len(sys.argv) > 3:
  return sys.argv[3]
 return 'http://this.is.api/services.json'

def getApiVersion(coinID):
 uapi = apiArg()
 r = requests.get(uapi)
 if r.status_code == 200:
  for w in r.json()['wallets']:
   if w['id'] == coinID:
    return w
  print('API dont have the coin: '+coinID)
  sys.exit(0)
 print('API link may not be available')  
 sys.exit(0)

def checkWalletVersion(rpcConn,apiVer):
 info = rpcConn.getinfo()
 if info:
  if info['version'] < apiVer:
   return 1
 return 0

def stopWallet(rpcConn):
 rpcConn.stop()

def usage():
 if len(sys.argv) < 3:
  print('Usage: ',sys.argv[0],' coin-id wallet-rpc api-update-nr')
  print('* nr -> not required, you must edit in script file')
  sys.exit(0)

usage()
coinID = sys.argv[1]
apiWallet = getApiVersion(coinID)
rpcConn = AuthServiceProxy(sys.argv[2])
if checkWalletVersion(rpcConn, apiWallet['version']) == 1:
 ver = str(apiWallet['version'])
 link = apiWallet['link']
 daemon = apiWallet['daemon']
 print('New update for coin: '+coinID+' -- version: '+ver)
 stopWallet(rpcConn)
 runUpdate(ver,link,daemon)
 sys.exit(0)
print('No update availale')

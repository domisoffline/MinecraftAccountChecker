import requests
from requests.api import head, request
import os
from colorama import init, Style, Fore
from datetime import datetime
init()
failedToLogin = True
debugmode = False # Warning! Enabling This Will Expose Your Auth Keys, Tokens are Other Sensitive Info in the Console. Because of this, it is recommended you leave this off for normal usage.
token = ''
with open('.\\valid.txt', 'w+') as f:
    f.truncate()
failedToLogin = False
canlogin = []

if os.path.getsize('.\\accounts.txt') > 0:
    pass
else:
    print(f"{Fore.RED}[FAIL]{Style.RESET_ALL} | Please enter accounts in proper format in accounts.txt file")
    os.abort()

def accessToken(proxy):
    global token
    global failedToLogin
    payloads = {
    "agent" : "minecraft",
    "username" : email,
    "password" : password,
    "requestUser" : "true"
    }

    headers = {
        "Content-Type" : "application/json"
    }
    responseJSON = requests.post("https://authserver.mojang.com/authenticate", json=payloads, headers=headers, proxies={'http' : f'{proxy}'})
    response_json = responseJSON.json()
    try:
        token = response_json['accessToken']
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} | Successfully logged into {email}")
        if debugmode == True:
            print(response_json)
        failedToLogin = False
        canlogin.append(email)
        with open('.\\valid.txt', 'a') as f:
            f.write(f'{email}:{password}\n')
        pass
    except:
        failedToLogin = True
        print(f"{Fore.RED}[FAIL]{Style.RESET_ALL} | Failed to login to {email}")
        if debugmode == True:
            print(response_json)
        pass

def getUsername(proxy):
    global username
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    r = requests.get("https://api.minecraftservices.com/minecraft/profile", headers=headers, proxies={'http' : f'{proxy}'})
    try:
        username = r.json()['name']
    except:
        username = 'Error Trying To Get Username'


def checkNameChange(proxy):
    global namechange
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    r = requests.get("https://api.minecraftservices.com/minecraft/profile/namechange", headers=headers, proxies={'http' : f'{proxy}'})
    if failedToLogin != True:
        if r.json()['nameChangeAllowed'] == True:
            namechange = True
            print(f'TEST {email}')
            if debugmode == True:
                print(r.json())
        elif r.json()['nameChangeAllowed'] == False:
            namechange = False
            if debugmode == True:
                print(r.json())
        else:
            print(f"{Fore.RED}[FAIL]{Style.RESET_ALL} | Encountered an unexpected error when trying to get info for account: {email}")
            if debugmode == True:
                print(r.json())
    else:
        pass

    r = requests.get("https://api.minecraftservices.com/minecraft/profile/namechange", headers=headers, proxies={'http' : f'{proxy}'})
with open('.\\accounts.txt', 'r') as f:
    proxynum = 0
    for line in f:
        email, password = line.split(':')
        email = email.strip()
        password = password.strip()
        with open('.\\proxies.txt', 'r') as proxyfile:
            lineproxy = proxyfile.readlines()[proxynum]
            try:
                accessToken('http://' + lineproxy + '/')
                if debugmode == True:
                        print(f'Proxy Used: {lineproxy}')
                proxynum = proxynum+1
                if failedToLogin == False:
                    getUsername('http://' + lineproxy + '/')
                    if debugmode == True:
                        print(f'Proxy Used: {lineproxy}')
                    proxynum = proxynum+1
                checkNameChange('http://' + lineproxy + '/')
                if debugmode == True:
                        print(f'Proxy Used: {lineproxy}')
                proxynum = proxynum+1
                if failedToLogin == False:
                    if namechange == True:
                        namechange = 'True'
                    else:
                        namechange = 'False'
                if failedToLogin == False:
                    print(f"""
    Email: {email}
    Password: {password}
    Username: {username}
    Namechange: {namechange}
                    """)
                proxynum = proxynum+1
            except:
                pass
print(str(canlogin))
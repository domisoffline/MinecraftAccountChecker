import requests
from requests.api import head, request
import os
from colorama import init, Style, Fore
from datetime import datetime
init()
with open('C:\\Users\\Dominic\\OneDrive - Brunswick Secondary College\\Desktop\\Code\\Minecraft\\vaild.txt', 'w+') as f:
    f.truncate()
failedToLogin = False
canlogin = []
try:
    if os.path.getsize('C:\\Users\\Dominic\\OneDrive - Brunswick Secondary College\\Desktop\\Code\\Minecraft\\accounts.txt') > 0:
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
            # print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} | Successfully logged into {email}")
            return True
        except:
            failedToLogin = True
            print(f"{Fore.RED}[FAIL]{Style.RESET_ALL} | Failed to login to {email}")
            pass

    def checkNameChange():
        headers = {
            "Authorization" : f"Bearer {token}"
        }
        r = requests.get("https://api.minecraftservices.com/minecraft/profile/namechange", headers=headers)
        if failedToLogin != True:
            if r.json()['nameChangeAllowed'] == True:
                print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} | Account: {email} can namechange!")
                canlogin.append(email)
                with open('C:\\Users\\Dominic\\OneDrive - Brunswick Secondary College\\Desktop\\Code\\Minecraft\\vaild.txt', 'a') as f:
                    f.write(f'{email}:{password}\n')
            elif r.json()['nameChangeAllowed'] == False:
                print(f"{Fore.RED}[FAIL]{Style.RESET_ALL} | Account: {email} cannot namechange!")
            else:
                print(f"{Fore.RED}[FAIL]{Style.RESET_ALL} | Encountered an unexpected error when trying to get info for account: {email}")
        else:
            pass
    with open('C:\\Users\\Dominic\\OneDrive - Brunswick Secondary College\\Desktop\\Code\\Minecraft\\accounts.txt', 'r') as f:
        for line in f:
            email, password = line.split(':')
            email = email.strip()
            password = password.strip()
            accessToken()
            checkNameChange()
except:
     print(f"{Fore.RED}[FAIL]{Style.RESET_ALL} | Unexpected Error Occurred When Attempting To Run Program.")
import os
import platform
import requests
import subprocess
import sys
import time

filetype = True
while filetype:
    print(
        """
1. Toontown Corporate Clash
2. Toontown Fellowship
3. Exit
    """
    )
    filetype = input("What would you like to do? ")
    if filetype == "1": #Toontown Corporate Clash
        CLASH_GAMESERVER = 'gs.corporateclash.net' #Corporate Clash Game Server
        CLASH_LOGIN_API = 'https://corporateclash.net/api/v1/login/' #Corporate Clash Login Server

        CLASH_USERNAME = input("Username: ") #Ask for Corporate Clash Username
        CLASH_PASSWORD = input("Password: ") #Ask for Corporate Clash Password

        response = requests.post(CLASH_LOGIN_API + CLASH_USERNAME, data = {'password': CLASH_PASSWORD}).json() #Send POST Request for playcookie

        if response['status']: #If successful
            print('Login success. Server gave token ' + response["token"] + "! " + str(response['friendlyreason'])) #Print the token and the response reason
            print("Launching the game...") #Print launching game
            os.chdir(os.getenv('LOCALAPPDATA') + '/Corporate Clash') #Open the clash directory
            subprocess.run(r'CorporateClash.exe', env = dict(os.environ, TT_GAMESERVER = CLASH_GAMESERVER, TT_PLAYCOOKIE = response["token"])) #Launch the game
            sys.exit(0)
        else:
            print('Login failed. Server gave status ' + str(response['reason']) + ' (' + str(response['friendlyreason']) + ')') #If not success, print and dump process
            sys.exit(2)
    
    elif filetype == "2": #Toontown Fellowship
        FELLOWSHIP_MANIFEST = 'https://toontownfellowship.com/download/manifest.json' #Fellowship Manifest
        FELLOWSHIP_LOGIN_API = 'https://reg.toontownfellowship.com/api/login' #Fellowship Login Server

        FELLOWSHIP_USERNAME = input("Username: ") #Ask for Fellowship Username
        FELLOWSHIP_PASSWORD = input("Password: ") #Ask for Fellowship Password

        payload = {'user': FELLOWSHIP_USERNAME, 'pass': FELLOWSHIP_PASSWORD} #Setup a payload for querying the placycookie
        response = requests.post(FELLOWSHIP_LOGIN_API, params=payload) #Send POST Request for playcookie
        fellowship_login_data = response.json() #scrape the returned JSON Output
        
        response = requests.get(FELLOWSHIP_MANIFEST) #Send GET Request for gameserver
        fellowship_gameserver_info = response.json() #scrape the returned JSON Output

        FELLOWSHIP_GAMESERVER = fellowship_gameserver_info['game-server'] #Load Fellowship's Gameserver
        FELLOWSHIP_TOKEN = fellowship_login_data["token"] #Token format
        
        if fellowship_login_data["result"] == "OK": #If token is sound
            print('Login success. Server gave token ' + (FELLOWSHIP_TOKEN) + "!") #Print the token
            print("Launching the game...") #Print launching game
            os.chdir('C:\Toontown Fellowship') #Open the TTF Directory
            subprocess.run(r'fellowship.exe', env = dict(os.environ, TTI_GAMESERVER = FELLOWSHIP_GAMESERVER, TTF_GAMESERVER = FELLOWSHIP_GAMESERVER, TTI_PLAYCOOKIE = FELLOWSHIP_USERNAME + ":" + FELLOWSHIP_TOKEN, TTF_PLAYCOOKIE = FELLOWSHIP_USERNAME + ":" + FELLOWSHIP_TOKEN)) #Launch the game
            sys.exit(0)
        else:
            print('Login failed. Server gave status (' + fellowship_login_data["result"] + ')') #If not success, print and dump process
            sys.exit(2)
    elif filetype == "3":
        print("\nGoodbye")
        filetype = None
    else:
        print("\nTry Again")

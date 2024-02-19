import os
import colorama
from colorama import Fore, Back, Style
import subprocess
import getpass
import re
import sys
import time
#import ipcalc

# Import all lib
from lib import addUser, updatePostgres, upgrade, installTools, cleanup

# To confirm Linux distribution in /etc/os-release
def get_distroName():
    try:
        with open('/etc/os-release', 'r') as os_release_file:
            for line in os_release_file:
                if line.startswith('ID='):
                    distro = line.split('=')[1].strip().strip('"')
                    # Extact distribution name and remove quotes
                    return distro
                
    except FileNotFoundError:
        print(Fore.RED + f'Could NOT confirm Linux Distribution...\nSkipping...\n')
        return None

# Move distroName outside the function
distroName = get_distroName()

#distroName = f"Current distro name is: {getDistro}"
#print(Fore.MAGENTA + distroName)
echoDistroName = f"Current distro name is :{distroName}"
print(Fore.MAGENTA + echoDistroName)
#print(type(distroName))

# A function to return all essential Python modules
def initializeModules():
    global os, Fore, Back, Style, getpass, subprocess, re

    # Initialize colorama
    colorama.init(autoreset=True)

    return os, Fore, Back, Style, getpass, subprocess, re
    # Initialize all modules

# Getting ROOT priviledge from users to allow sudo actions
def getCredentials():
    try:
        print(Fore.WHITE + "\nProceeding...\n")
        get_user = f'whoami'
        doGetUser = subprocess.Popen(get_user, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        doGetUser_out, doGetUser_err = doGetUser.communicate()
        user = doGetUser_out
        sudo_password = getpass.getpass(prompt='Enter sudo password: ')
        return user, sudo_password

    except Exception as e:
        # Handle exceptions
        print(Fore.RED + f'Error retrieving root credentials from script user: {str(e)}')
        print(Fore.RED + 'Terminating script running & all Shell processes...\n')
        sys.exit()

# Returning user, sudo_password from getCredentials()
user, sudo_password = getCredentials()

def getTime():
    try:
        # Get current local time as a struct time OBJ
        current_time = time.localtime()
        formatted_time = time.strftime('%Y-%m-%d-%H:%M:%S', current_time)
        return formatted_time
    
    except Exception as e:
        print(Fore.RED + f'Failed to retrieve current time :(\n')
formatted_time = getTime()
    

confirmAddUser = input("Do you wanna add a new priviledged user? [Y/N]: ")

# Passing newUser, newPassword inputs from passingUser() to this.module
#newUser,newPassword = passingUser()

# To update PostgreSQL 15 && 14 TCP ports (5432 && 5433)
confirmUpdatePostgres = input("Do you wanna update PostgreSQL14 & 15 ports 5432? [Y/N]: ")
   
    
# To update http.kali.org => https.kali.org
confirmUpgrade = input("Do you wanna upgrade apt & kali repo? [Y/N]: ").strip()    

## For installing open-source tools
confirmInstallTools = input("Do you wanna install tools? [Y/N]: ")

# Whether addUser()
if confirmAddUser.lower == 'y':
    # Adding a new privileged user
    # Sanity checks
    newUser = input("Enter new privileged user name: ")
    newPassword = getpass.getpass("Enter your new privileged user password: ")
    confirmNewPassword = getpass.getpass("Enter your new privileged user password: ")
    # Default match = False
    match = False

    if newPassword == confirmNewPassword:
        match = True
        print(Fore.YELLOW + "Will add a new privileged user for you :)")
        # If newPassword == confirmNewPassword
        # Run addUser() callback from ./lib/addUser.py
        addUser.addUser(user, sudo_password, newUser, newPassword, formatted_time)
        pass
        #return newUser, newPassword
    else:
        #match = False
        print(Fore.YELLOW + f'NOT gonna add a new priviledged user\nSkipping...\n')
        #return None, None
else:
    print(Fore.YELLOW + f'NOT gonna add a new priviledged user\nSkipping...\n')
    #return None, None
    
# Whether updatePostgresql()
if confirmUpdatePostgres.lower() == 'y':
    print(Fore.YELLOW + f'Will update postgreSQL 15 & 14 ports :)...\n')
    updatePostgres.updatePostgres(user, sudo_password, formatted_time)
    pass    
else:
    print(Fore.YELLOW + f'NOT gonna update postgreSQL 15 & 14 ports\nSkipping...\n')    
    
# Whether upgrade()
if confirmUpgrade.lower() == 'y':
    print(Fore.YELLOW + f'\n\nWill update Kali repository connection using HTTPS\nto allow apt update && apt upgrade\n\n')
    upgrade.upgrade(user, sudo_password, formatted_time)
    pass
else:
    print(Fore.YELLOW + f'\n\nWill NOT update Kali repository\n\nYou have to manually edit Kali repository config file\nhttp://kali.org => https://kali.org\nAND update the Kali keys from Kali archive\nin order to get apt install functions working...\n\n')
    #confirmUpgrade = 'n'

# Whether installTools()
if confirmInstallTools.lower() == 'y':
    print(Fore.YELLOW + f'Will install Open-source tools for you ;)')
    print(f'\n')
    print(f'Package managers\n[e.g. Python3-pip, SNAP, GEM, NixNote2, Nautilus-dropbox, Keepassxc, DNF\n')
    print(Fore.YELLOW + f'')
    installTools.installTools(user, sudo_password, formatted_time)
    pass
else:
    print(f'\n')
    print(Fore.YELLOW + f'NOT want to install open-source tools\nSkipping...')
    print(f'\n')
    print(f'\n')
    
## For customizing a NIC
# confirmNetworking = input("Do you wanna configure a network interface? [Y/N]: ")
# def passingNetworking():
#     if confirmNetworking and confirmNetworking.lower() == 'y':
#         print(Fore.YELLOW + f'\nWill set up a NIC for you :)\n')
#         return confirmNetworking
#     else:
#         print(Fore.YELLOW + f'\nNot gonna set up a NIC\nSkipping...\n')
# confirmNetworking = passingNetworking()

## For customizing Keyboard Layout
# confirmChangeKeyboardLayout = input("Do you wanna change keyboard layout? [Y/N]: ")
# def passingKeyboard():
#     if confirmChangeKeyboardLayout and confirmChangeKeyboardLayout.lower() == 'y':
#         print(Fore.YELLOW + f'\nWill change keyboard layout :)\n')
#         return confirmChangeKeyboardLayout
#     else:
#         print(Fore.YELLOW + f'\nNot gonna change keyboard layout\n')
# confirmChangeKeyboardLayout = passingKeyboard()


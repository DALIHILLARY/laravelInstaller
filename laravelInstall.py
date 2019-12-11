#!/usr/bin/env python3

#this project was inspired by the hardish in BSSE students in my University installing laravel on linux/mac
#please do not run script as root for better functionality

#let us import the modules required for the script
import requests
import progressbar
import re
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.request import urlretrieve
import os
import shutil

#split the logic into functions

class MyProgressBar():
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar=progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()


def Xampp():
    #check if xampp install path exists
    
    dir = Path("/opt/lampp/")
    if not dir.exists():
        choice = str(input("Do you have xampp file on computer (YES,NO):"))
        if choice in ['yes','YES','y','Y']:
            print("Please move the file to  %s \n" %os.getcwd())
            
            input("PRESS ANY KEY WHEN COPY IS DONE:")
            os.system("mv *.run xampp.run")
       
        
        else:
                url = 'https://www.apachefriends.org'
                dst = 'xampp.run'
                r = requests.get(url)
                soup = BeautifulSoup(r.text,'html.parser')
                for x in soup.findall('a'):
                        link = x.get('href') #extract href links from results
                        if re.search("xampp-linux",link): #search for linux in links
                                url = link #assign url to the link gotten

                print("\033[31m.............DOWNLOADING XAMPP PLEASE WAIT...............")
                urlretrieve(url,dst,MyProgressBar())
        #instructions to execute after decision making 
        os.system("echo %s | sudo -S chmod +x xampp.run" %pwd)
        os.system("echo %s | sudo -S ./xampp.run" %pwd)
        os.system("echo %s | sudo -S ln -s /opt/lampp/bin/php /usr/local/bin/php" %pwd)
        os.system("echo %s | sudo -S /opt/lampp/xampp start" %pwd)

    else:
        print("\n xampp install already existing. installing other requirements ..... \n \n")

def composer():
    #this will check if composer exists and unistall it then re-install it
    print("\n performing actions on composer....")
    user = os.listdir("/home")
    user = user[0]
    x = "/home/"+ user
    x+="/.config/composer"
    w = "/home/"+ user + "/.composer"
    compUbuntu = Path(w)
    if compUbuntu.exists():
            print("\n removing composer folder \n")
            os.system("echo %s | sudo -S rm -rf %s" %(pwd,w))

    compInstall = Path(x)
    if compInstall.exists():
        print("\n removing composer folder \n")
        shutil.rmtree(x)
    dir = "/home/"+ user
    os.chdir(dir)
    print(" \n installing composer")

    #parsing the download page
    url = "https://getcomposer.org/download/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    cinst = soup.pre.string #composer download code in <pre> tags
    os.system(cinst)
    os.system("echo %s | sudo -S mv composer.phar /usr/local/bin/composer" %pwd)
    print("\033[31m \n ...........CREATING LARAVEL PROJECT.... PLEASE WAIT \033[31m")

    #check if user has git installed
    git = Path("/bin/git")
    if not git.exists():
        os.system("echo %s | sudo -S apt-get install git" %pwd)
        
    os.system("composer create-project --prefer-dist laravel/laravel %s" %name)
    os.chdir("%s" %name)
    os.system("php artisan serve")

def banner():
    logo = ''' \033[32m
        **************************************************************** 
                ***    ****    *****   *****         *****
                ***    ****    *****     *****      *****
                ***    ****    *****       *****   *****
                ***********    *****         **** ****  
                ***    ****    *****        *****  *****
                ***    ****    *****       *****     *****
                ***    ****    *****     *****        *****
        **************************************************************** 
                       A LARAVEL INSTALLER BY KALI HIX 
                        PROGRAMMERS OVER MORTAL-MEN
         \033[32m'''
    print(logo)

def env():
    #adding xampp php to local environment
    #just editing the /etc/environment file
    print("moving php to local path...... ")
    os.system("echo %s | sudo -S ln -s /opt/lampp/bin/php /usr/local/bin/php")
    instpath = 'PATH=("/opt/lampp/bin/php:'
    os.system("echo | cat /etc/environment > environment.txt")
    with open("environment.txt","r+") as lpath:
        x =''
        for line in lpath:
                x = line.split('"')[1]
                x = instpath + x
                x+= '")'
        lpath.seek(0)
        lpath.truncate(0)
        lpath.write(x)
        lpath.close()
    os.system("echo %s | sudo -S mv environment.txt /etc/environment")
    print("done")

        
#let us fire up this project......

if __name__ == '__main__':
        banner()
        if os.geteuid() != 0:
                
                name = str(input("\033[32m PLEASE ENTER THE NAME OF THE PROJECT: \033[32m"))
                pwd  = str(input("\n PLEASE ENTER PC PASSWORD:"))

                Xampp()
                env()
                composer()

        else:
                print(" \033[31m PLEASE DON'T RUN SCRIPT AS ROOT \033[31m")


    

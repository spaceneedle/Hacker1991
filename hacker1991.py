import code
import sys
import sqlite3
import time
import threading
import random
import sqlite3
import imp
import os

# check for pyaudio

try:
    imp.find_module('pyaudio')
    pa = True
except ImportError:
    pa = False

if pa == True: import pyaudio


# TODO: turn on character by character mode on terminal

# game variable defaults

name = "n/a"
location = "n/a"
motto = "n/a"
prompttext = "%"						# command line prompt
modem = 300						# default modem speed of 300 baud
dir = "/"						# current directory
wardialer = 0						# wardialer status (0 = off, 1 = dialing)
level = 0						# current game level
bytecoins = 0						# in game currency
gfx = "monochrome_monitor"
sound = "PC_Speaker"
storage = 1544
drive = "floppy_drive"
miner = "MinerLite_ASIC"
miner_rate = 100
miner_state = 0
points = 0
bbsfound = 0
wardials = 0
bbscalls = 0
bbsbattles = 0
pvpbattles = 0
wins = 0
losses = 0
downloads = 0
lan = 0
lan_address = "00:00:00:00"
kill = 0						# kill thread
offline = False						# all text is considered online mdoe

viruses_inventory = []
skill_inventory = []

viruses_inventory.append("Rogue")
skill_inventory.append("BBS Dialing")
skill_inventory.append("ByteCoin Mining")
skill_inventory.append("Wardialing")

viruses = len(viruses_inventory)
skills = len(skill_inventory)

# database 

try:
    global conn
    global c
    conn = sqlite3.connect('hacker.db')
    c = conn.cursor()
except:
    print "ERROR: Cannot find game database. Exiting."
    quit()

# additional audio support 

def playAudio(file):
   os.system("afplay "+str(file)+" &")

# terminal functions for easy remapping to TCP or other I/O

def clearScreen():
   sayshort("\033[2J")  
   sayshort("\033[#;#H")

def _green():
   sayshort("\033[1;32;40m")

def modem_char():
    time.sleep(1.0/modem)

def send(text):
   for i in range(0,len(text)):
      sys.stdout.write(text[i])
      sys.stdout.flush()
      modem_char()

def say(text):
   if offline == True: print text
   else: send(text+"\n")

def sayshort(text):
   if offline == True: 
            sys.stdout.write(text)
            sys.stdout.flush()
   else: send(text)

def prompt(text):
   return raw_input(text)

def waitchar(Block=True):
  if Block or select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
    return sys.stdin.read(1)
  raise error('NoChar')

# threads 
# TODO: get this working with threading, tweak the random lottery so it makes sense

def miner_thread():
   global miner_rate
   global bytecoins
   global miner_state
   global kill
   while 1==1:
     while miner_state == 1:
          time.sleep(1/miner_rate)  
          a = random.randint(0,10)
          b = random.randint(0,10)
          if a == b: bytecoins = bytecoins + 1
          if kill == 1:
               say("SIG_KILL: Mining stopped. Miner thread halting.")
               return
     time.sleep(1)
     if kill == 1:
               say("SIG_KILL: Mining already stopped. Miner thread halting.") 
               return

def titleAscii():
 say("                                                                              ")
 say("                                                                              ")
 say('  ___ ___                __                   ____ ________  ________  ____   ')
 say(' /   |   \\_____    ____ |  | __ ___________  /_   /   __   \\/   __   \\/_   |  ')
 say('/    ~    \\__  \\ _/ ___\\|  |/ // __ \\_  __ \\  |   \\____    /\\____    / |   |  ')
 say('\\    Y    // __ \\\\  \\___|    <\\  ___/|  | \\/  |   |  /    /    /    /  |   |  ')
 say(' \\___|_  /(____  /\\___  >__|_ \\\\___  >__|     |___| /____/    /____/   |___|  ')
 say('       \\/      \\/     \\/     \\/    \\/                                         ')
 say("                                                                              ")
 say("                                                                              ")
 say("By: MaoKHiaN                                                                  ")
 say("                                                                              ") 


# intro

def intro():
  global name
  global motto
  global location
  playAudio("intro1.wav")
  _green()
  clearScreen()
  time.sleep(1)
  sayshort("Memory check...")
  offline = True
  for i in range(0,31000,256):
     sayshort(str(i))
     sayshort("\033[0;0fMemory check...")
  offline = False
  titleAscii()
  sayshort("Press enter to start")
  waitchar()
  sayshort("Installing operating system image.....")
  time.sleep(3)
  say("[DONE]")
  say("Booting operating system.....")
  time.sleep(2)
  sayshort("Hardware discovery: ")
  time.sleep(2)
  sayshort("Supra_300_baud_modem ")
  time.sleep(0.75)
  sayshort("MinerLite_ASIC ")
  time.sleep(1)
  sayshort("floppy_drive ")
  time.sleep(0.5)
  sayshort("keyboard ")
  time.sleep(0.5)
  sayshort("monochrome_monitor ")
  time.sleep(0.6)
  say("PC_Speaker")
  say("Entering multiuser mode...")
  time.sleep(2)
  say("ADD_USER()")
  name = prompt("User name: ")
  location = prompt("Location: ")
  motto = prompt("Motto [Optional]: ")
  ## TODO: populate database with these values 

# Game functions


# directory listing
## TODO: make this database driven so the user can install applications over time

def ls(command):
  arg = command.split(" ")
  format = "basic"
  hidden = 0
  if len(arg) > 1:
      if arg[1][0] == "-":
        for i in range(0,len(arg[1])):
          if arg[1][i] == "l": format = "list"
          if arg[1][i] == "a": hidden = 1
  if dir == "/":
   if format == "basic":
     if hidden == 1:
           sayshort(". .. ")
     say("terminal wardialer mine stats")
     return 
   if format == "list":
     if hidden == 1:
       say("drwxr-xr-x   3 staff  staff      96 May 21 11:20 .")
       say("drwxr-xr-x  23 staff  staff     736 May 21 11:26 ..")
     say("drwxr-xr-x   1 staff  staff      22 Jan 01 23:05 downloads")
     say("drwxr-xr-x   1 staff  staff     499 Jan 01 23:05 bin")
     say("-rwxr-xr-x   1 staff  staff  131797 May 21 11:46 terminal")
     say("-rwxr-xr-x   1 staff  staff  263122 May 21 11:46 wardialer")
     say("-rwxr-xr-x   1 staff  staff  765314 May 21 11:46 mine")
     say("-rwxr-xr-x   1 staff  staff   56236 May 21 11:46 stats")

def python(command):
  banner="code.interact session, type Ctrl-Z to exit."
  code.interact( banner=banner)

def terminal(command):
     print "TBD"

def mine(command):
     global bytecoins
     global miner_rate
     global miner_state
     sayshort("attaching to miner hardware...")
     time.sleep(1)
     say("CONNECTED")
     while 1==1:
        say("+=======================+")
        say("| ByteCoin Miner Menu   |")
        say("+-----------------------+")
        sayshort("Miner State : ")
        if(miner_state == 0):
           say("off")
        else:
           say("ON")
        sayshort("ByteCoins   : ")
        say(str(bytecoins))
        sayshort("Hardware    : ")
        say(str(miner))
        sayshort("Mining Rate : ")
        say(str(miner_rate))
        say("------------------------")
        say("1) Toggle mining state")
        say("2) Exit")
        i = prompt("==> ")
        if i == "1":
            if miner_state == 0:
                    miner_state = 1
            else:
                    miner_state = 0
        if i == "2":
            break 

def stats(command):
     say("============ Stats ============")
     say("name        : "+str(name))
     sayshort("LAN Address : ")
     if lan == 1:
        say(lanaddress)
     else:
        print "Not installed"
     say("location    : "+str(location))
     say("motto       : "+str(motto))
     say("modem       : "+str(modem))
     say("graphics    : "+str(gfx))
     say("sound       : "+str(sound))
     say("drive       : "+str(drive))
     say("storage     : "+str(storage)+" kB")
     say("points      : "+str(points))
     say("BBSes Found : "+str(bbsfound))
     say("Wardials    : "+str(wardials))
     say("BBS calls   : "+str(bbscalls))
     say("BBS Battles : "+str(bbsbattles))
     say("Wins        : "+str(wins))
     say("Losses      : "+str(losses))
     say("PVP Battles : "+str(pvpbattles))
     say("Downloads   : "+str(downloads))
     say("--------------------------------------------------------------")
     sayshort("Skills ("+str(len(skill_inventory))+"): ")
     for i in range(0,len(skill_inventory)):
         sayshort(skill_inventory[i]+", ")
     say("\n--------------------------------------------------------------")
     sayshort("Viruses ("+str(len(viruses_inventory))+"): ")
     for i in range(0,len(viruses_inventory)):
         sayshort(viruses_inventory[i]+", ")
     say("\n--------------------------------------------------------------")
     say("You have "+str(bytecoins)+" ByteCoins")

def wardialer(command):
     print "TBD" 

# Command shell
# TODO: database driven based on level, downloaded apps, etc.
# support arguments properly

def shelly():
  global kill
  while 1==1:
   fullcmd = raw_input(prompttext+" ")
   command = fullcmd.split(" ")[0]
   if command == "wardialer":
        wardialer(fullcmd)
   elif command == "ls":
        ls(fullcmd)
   elif command == "python":
        python(fullcmd)
   elif command == "terminal":
        terminal(fullcmd)
   elif command == "stats":
        stats(fullcmd)
   elif command == "cd":
        cd(fullcmd)
   elif command == "mine":
        mine(fullcmd)
   elif command == "exit":
        ## TODO: save user progress
        say("Stopping miner thread...")
        kill = 1
        time.sleep(2)
        say("Logging out...")
        time.sleep(2)
        os.system("reset")
        quit()
   elif command == "save":
        ## TODO: save user progress
        say("Saving not supported yet")
   else:
        say("error: unknown command "+str(command))

## TODO: provide user/password prompt or new user ability

intro()

# start threads

threading.Thread(target=miner_thread).start()

# start main loop in game

shelly()


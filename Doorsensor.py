#
#  DoorSensor.py
#
#  Copyright 2020  <pi@raspberrypi>
#
# Basically I'm attempting to create a program that would run on a raspberry pi and act check for the status
# on a door sensor connected to the GPIO pins and upload said status to html files stored where nginx
# html files would be stored
# the details of this project will obviously not plug into every pi so be sure to change the file url's
# into ones relevant in your case
#

import RPi.GPIO as GPIO
import time
import threading
import datetime
import sched
#Setting broadcom so GPIO can be adressed by number
GPIO.setmode(GPIO.BOARD)

#Set up door sensor pin.
#the door sensor should be attached to this pin.
#and another to a ground pin 6,9,14,20,25,30,34,39
GPIO.setup(8, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# a time function for the timer
global Door_status
global end_time
global start_time
global current_time
Door_status = False
Door_Status_two = None
current_time = 0
start_time = 0
end_time = 0
def time_convert(sec):
        mins = sec / 60
        sec = sec % 60
        hours = mins / 60
        mins = mins % 60
        global current_time
#Now for the actual program logicS
def returnLongStatus():
        global end_time
        global start_time
        time_lapsed = float(end_time) - float(start_time)
        time_convert(time_lapsed)
        end_time = 0
        start_time = 0

s = sched.scheduler(time.time, time.sleep)
def GetDoorStatus():
        global Door_status 
        return Door_status
        
def Print_toHTML_OPEN():
        if GetDoorStatus() == True:
                webpage = open('/var/www/html/index.html', 'w')
                webpage.write('<!DOCTYPE html> \n')
                webpage.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n')
                webpage.write('<meta http-equiv="refresh" content="10" url=index.html">\n')
                webpage.write('<head>\n')
                webpage.write('<title>Bathroom Status</title>\n')
                webpage.write('</head>\n')
                webpage.write('<body>\n')
                webpage.write('<h1>The bathroom is currently: <h1 style="color:green">OPEN<h1></h1>\n')
                webpage.write('<iframe style="border:none" src="index1.html"></iframe>')
                webpage.write('</body>\n')
                webpage.write('</html>')
                webpage.close()
        if GetDoorStatus() == False:
                webpage = open('/var/www/html/index.html', 'w')
                webpage.write('<!DOCTYPE html> \n')
                webpage.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n')
                webpage.write('<meta http-equiv="refresh" content="4" url=index.html">\n')
                webpage.write('<head>\n')
                webpage.write('<title>Bathroom Status</title>\n')
                webpage.write('</head>\n')
                webpage.write('<body>\n')
                webpage.write('<h1>The bathroom is currently: <h1 style="color:green">OPEN<h1></h1>\n')
                webpage.write('<iframe style="border:none" src="index1.html"></iframe>')
                webpage.write('</body>\n')
                webpage.write('</html>')
                webpage.close()

def Print_toHTML_CLOSED():
        if GetDoorStatus() == False:
                webpage = open('/var/www/html/index.html', 'w')
                webpage.write('<!DOCTYPE html> \n')
                webpage.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n')
                webpage.write('<meta http-equiv="refresh" content="33" url=index.html">\n')
                webpage.write('<head>\n')
                webpage.write('<title>Bathroom Status</title>\n')
                webpage.write('</head>\n')
                webpage.write('<body>\n')
                webpage.write('<h1>The bathroom is currently: <h1 style="color:red">CLOSED<h1></h1>\n')
                webpage.write('<iframe style="border:none" src="index1.html"></iframe>')
                webpage.write('</body>\n')
                webpage.write('</html>')
                webpage.close()
        if GetDoorStatus() == True:
                webpage = open('/var/www/html/index.html', 'w')
                webpage.write('<!DOCTYPE html> \n')
                webpage.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n')
                webpage.write('<meta http-equiv="refresh" content="4" url=index.html">\n')
                webpage.write('<head>\n')
                webpage.write('<title>Bathroom Status</title>\n')
                webpage.write('</head>\n')
                webpage.write('<body>\n')
                webpage.write('<h1>The bathroom is currently: <h1 style="color:red">CLOSED<h1></h1>\n')
                webpage.write('<iframe style="border:none" src="index1.html"></iframe>')
                webpage.write('</body>\n')
                webpage.write('</html>')
                webpage.close()

def GetEndTime():
        global end_time 
        return end_time
        
def GetStartTime():
        global start_time 
        return start_time

def SetDoorStatus(variable):
        global Door_status
        Door_status = variable
        
def checkDoor():
#Bunch of Booleans to hold the status of the door
    if GPIO.input(8) == True:
        if GetDoorStatus() == True:
                webpage = open('/var/www/html/index1.html', 'w')
                webpage.write('<!DOCTYPE html> \n')
                webpage.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n')
                webpage.write('<head>\n')
                webpage.write('<script text="text/javascript"> \n')
                webpage.write('window.onload= function(){ \n')
                webpage.write('document.getElementById("audio_two").play(); \n')
                webpage.write('} \n')
                webpage.write('</script> \n')
                webpage.write('</head>\n')
                webpage.write('<body>\n')
                webpage.write('<audio id="audio_two" src="ToiletFlush.mp3"></audio>\n')
                webpage.write('</body>\n')
                webpage.close()
                Print_toHTML_OPEN()
                time.sleep(10)
                SetDoorStatus(False)
        elif GetDoorStatus() == False:
                webpage = open('/var/www/html/index1.html', 'w')
                webpage.write('<!DOCTYPE html> \n')
                webpage.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n')
                webpage.write('<head>\n')
                webpage.write('</head>\n')
                webpage.write('<body>\n')
                webpage.write('</body>\n')
                webpage.close()
        global end_time
        global start_time
        if start_time > 0:
                
                end_time += time.time()
                Print_toHTML_OPEN()
                time.sleep(1)
                returnLongStatus()
        else:
                end_time = 0
                Print_toHTML_OPEN()
                time.sleep(1)
    if GPIO.input(8) == False:
        # Create getters and seetters for startime and endtime
        if start_time == 0:
                start_time = time.time()
                current_time = time.ctime(start_time)
                Print_toHTML_CLOSED()
                if GetDoorStatus() == False:
                        webpage = open('/var/www/html/index1.html', 'w')
                        webpage.write('<!DOCTYPE html> \n')
                        webpage.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n')
                        webpage.write('<head>\n')
                        webpage.write('<script text="text/javascript"> \n')
                        webpage.write('window.onload = function(){ \n')
                        webpage.write('document.getElementById("audio_one").play(); \n')
                        webpage.write('} \n')
                        webpage.write('</script> \n')
                        webpage.write('</head>\n')
                        webpage.write('<body>\n')
                        webpage.write('bathroom closed at :' + str(current_time))
                        webpage.write('<audio id="audio_one" src="SpacecraftLaunch.mp3"></audio>\n')
                        webpage.write('</body>\n')
                        webpage.close()
                        time.sleep(33)
                        SetDoorStatus(True)
                elif GetDoorStatus() == True:
                        webpage = open('/var/www/html/index1.html', 'w')
                        webpage.write('<!DOCTYPE html> \n')
                        webpage.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n')
                        webpage.write('<head>\n')
                        webpage.write('</head>\n')
                        webpage.write('<body>\n')
                        webpage.write('bathroom closed at :' + str(current_time))
                        webpage.write('</body>\n')
                        webpage.close()
                time.sleep(1)
                s.enter(1,0,checkDoor,())
        elif end_time > 0:
                end_time = 0
                Print_toHTML_CLOSED()
                time.sleep(1)
                s.enter(1,0,checkDoor,())
        elif start_time > 0 and end_time > 0:
                start_time = 0
                Print_toHTML_CLOSED()
                time.sleep(1)
                s.enter(1,0,checkDoor,())
        else:
                Print_toHTML_CLOSED()
                time.sleep(1)
                s.enter(1,0,checkDoor,())
def door_function():
        while True:
                s.enter(1,0, checkDoor,())
                s.run()

threading.Thread(target=door_function).start()

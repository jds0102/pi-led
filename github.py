import requests
import json
import time
import sys
import signal

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

RED = 25

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RED,GPIO.OUT)



siqUrl = 'https://api.github.com/repos/infoseci/securityiq/pulls?type=open'
petraUrl = 'https://api.github.com/repos/infoseci/petra/pulls?type=open'

p = {'access_token': sys.argv[1]} 

def signal_handler(sig, frame):
        GPIO.cleanup()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

while True:

#  GPIO.output(RED,GPIO.HIGH)
#  time.sleep(1)
#  GPIO.output(RED,GPIO.LOW)

#  print ('Before siq req: ' + str(time.time()))
  siqRes = requests.get(siqUrl, params=p).json()
#  print ('Before petra req: ' + str(time.time()))
  petraRes = requests.get(petraUrl, params=p).json()

  prs_without_ass = 0
#  print ('Before loop: ' + str(time.time()))

  for pr in siqRes+petraRes:
    ass = pr.get('assignees', [])
    print(pr['title'] + ': ' +str(len(ass)))
    if len(ass) == 0:
      prs_without_ass += 1

  print (prs_without_ass)

  if prs_without_ass > 0:
    GPIO.output(RED,GPIO.HIGH)
  else:
    GPIO.output(RED,GPIO.LOW)

  time.sleep(15)

GPIO.cleanup()

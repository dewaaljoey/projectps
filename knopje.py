import RPi.GPIO as GPIO
import csv
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_UP)
start = 0
stop = 0
print("knopje")
while True:
	if stop - start > 0.2:
		print("add")
		task = 'add'
		with open('task.csv', 'w', newline='') as csvfile:
			spamwriter = csv.writer(csvfile)
			spamwriter.writerow(["add"])
	if GPIO.input(17) == 0:
		stop = time.time()
	if GPIO.input(17) ==1:
		start = time.time()

import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD
import csv
lcd = CharLCD(pin_rs = 26, pin_rw = 9, pin_e = 19, pins_data = [13,6,5,11], numbering_mode = GPIO.BCM)
import time
lcd.cursor_mode = "hide"
print("show")
def laat_zien(lijn1,lijn2,delay):
	x = 2
	scroll1 = False
	scroll2 = False
	
	if len(lijn1) > 16:
		scroll1 = True
		lijn1 = x*" " + lijn1 + x*" "
	if len(lijn2) > 16:
		scroll2 = True
		lijn2 = x*" " + lijn2 + x*" "
		
	hoogste = lijn2
	if len(lijn1) > len(lijn2):
		hoogste = lijn1
	if scroll1 == True or scroll2 == True:
		for teller in range(0,len(hoogste)-15):
			verander1 = lijn1
			verander2 = lijn2
			if scroll1 == True:
				verander1 = lijn1[teller:teller+16]
			if scroll2 == True:
				verander2 = lijn2[teller:teller + 16]
			#print(verander2)
			lcd.clear()
			lcd.write_string(verander1)
			lcd.cursor_pos = (1,0)
			lcd.write_string(verander2)
			time.sleep(delay)
	else:
		lcd.clear()
		lcd.write_string(lijn1)
		lcd.cursor_pos = (1,0)
		lcd.write_string(lijn2)
		time.sleep(1)
		#print(lijn1)
		#print(lijn2)
lcd.clear()
while True:
	file = open("result.csv")
	csvreader = csv.reader(file)
	lijst = []
	for row in csvreader:
		lijst = lijst + row
	#print(lijst)
	

	laat_zien(lijst[0],lijst[1],0.8)



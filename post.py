import requests
import sounddevice as sd
import os
from pydub import AudioSegment
from scipy.io.wavfile import write
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD
import time
import csv
print("post")
x = True
bluetooth = True
start = 0
stop = 0
lcd = CharLCD(pin_rs = 26, pin_rw = 9, pin_e = 19, pins_data = [13,6,5,11], numbering_mode = GPIO.BCM)
GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_UP)

while True:
    fs = 48000
    seconds = 3
    print("Recording...")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write('/home/pi/Documents/songs/file.wav', fs, myrecording)
    sound = AudioSegment.from_wav('/home/pi/Documents/songs/file.wav')
    sound.export('/home/pi/Documents/songs/file.mp3', format='mp3')
    print("Done.")
    os.remove("/home/pi/Documents/songs/file.wav")
    task = 'match'
    #add,match
    file = open("task.csv")
    csvreader = csv.reader(file)
    task = ""
    for row in csvreader:
        task = row

    with open('task.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(["match"])
    data = {'task': task}
    try:
        files = {'file': open(r'/home/pi/Documents/songs/file.mp3', 'rb'),}
        result = requests.post('http://192.168.0.37:8079/index', data=data,files=files)
        print(result.content)
        json = result.json()
        if json['result'] != None:
            with open('result.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile)
                spamwriter.writerow([json['result']['artist']])
                spamwriter.writerow([json['result']['title']])
            #lcd.clear()
            print(json)
            #lcd.write_string(json['result']['artist'])
            #lcd.cursor_pos = (1,0)
            #lcd.write_string(json['result']['title'])
    except:
        pass
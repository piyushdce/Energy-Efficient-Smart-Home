#!/usr/bin/env python3  

from server import SimpleHTTPRequestHandler, HTTPServer  
from server import BaseHTTPRequestHandler, HTTPServer  
import server
#import socketserver
import time
import threading
from w1thermsensor import W1ThermSensor
from gpiozero import MotionSensor
sensor = W1ThermSensor()
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
#GPIO.setup(15,GPIO.OUT) #led
GPIO.setup(24,GPIO.OUT) #relay
GPIO.setup(2,GPIO.OUT)  #LDR
pir = MotionSensor(21)

def run_server(HandlerClass=SimpleHTTPRequestHandler,port=8000):  
    print('http server is starting...')  
    #ip and port of servr  
    #by default http server port is 80  
    server_address = ('', port)  
    HandlerClass.protocol_version = "HTTP/1.0"
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)  
    print('http server is running...')  
    httpd.serve_forever()  
    print('Should not be printed')

def run_sensors():
    global BR1_L1
    global heater_temp
    global light_threshold
    global heater
    while True:
        time.sleep(1)
        temperature = sensor.get_temperature()
        print('temp: ', temperature)
        if server.mode:		# Automatic power saving mode
            GPIO.setup(2,GPIO.OUT)	#make GPIO dir as output in starting to discharge cap
            delay=0
            GPIO.output(2,GPIO.LOW)	#discharge capacitor
            time.sleep(0.5)
            GPIO.setup(2,GPIO.IN)	#change GPIO dir to sense voltage
            while (GPIO.input(2) == GPIO.LOW):
                delay = delay+1
            print('delay:',delay)
            if delay < 800:
                print('off loop')
                GPIO.output(24,GPIO.LOW)    #Ambient light enough. Don't turn on light.
                BR1_L1 = 0
            else:				#Ambient light low. Turn on light.
                GPIO.output(24,GPIO.HIGH)
                print('on loop')
                BR1_L1 = 1
            if temperature < heater_temp:   # Turn on heating
                GPIO.output(24,GPIO.HIGH)
                heater = 1
            else:   			    # Turn off heating
                GPIO.output(24,GPIO.LOW)
                heater = 0
        else:			# Manual Mode
            if server.light_on:
                GPIO.output(24,GPIO.HIGH)
                BR1_L1 = 1
            elif server.heater_on:
                GPIO.output(24,GPIO.HIGH)
                BR1_L1 = 1
            else:
                GPIO.output(24,GPIO.LOW)
                BR1_L1 = 0
        if pir.motion_detected:
            global motion_timer
            motion_timer = 0

def run_timers():	# Timer function. Handles global and local timers.
    while True:
        global motion_timer
        global heater_temp
        global light_threshold
        global BR1_L1
        print("motion_timer=  ",motion_timer)
        time.sleep(3)
        motion_timer+=1
        if motion_timer > 20:	# No one is at home. enable power saving.
            heater_temp = 10	# reduce heating to cool power.
            light_threshold = 8000  # increase light sensor threshold to save power.
        else:
            heater_temp = 24	# default value
            light_threshold = 800	#default value
        if BR1_L1:		# increment light1 on timer
            server.BR1_L1_on_time += 1
        if BR2_L2:		# increment light2 on timer
            server.BR2_L2_on_time += 1
        if heater:		# increment heater on timer
            server.heater_on_time += 1
        if ac:			# increment AC on timer
            server.ac_on_time += 1
     
motion_timer = 0   
BR1_L1 = 0
BR2_L2 = 0
heater = 0
heater_temp = 24
light_threshold = 800
ac = 0
if __name__ == '__main__':  
    #Handler = myhttphandler
    Handler = SimpleHTTPRequestHandler
    PORT = 8000
    print("serving at port", PORT)
    thread1 = threading.Thread(target=run_server, args=(Handler,PORT))
    #run_server(HandlerClass=Handler,port=PORT)  
    thread1.start()
    thread2 = threading.Thread(target=run_sensors)
    thread2.start()
    thread3 = threading.Thread(target=run_timers)
    thread3.start()
    

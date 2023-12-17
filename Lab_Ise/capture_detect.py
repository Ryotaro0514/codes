#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

PIR_OUT_PIN = 11    # pin11

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(PIR_OUT_PIN, GPIO.IN)    # Set BtnPin's mode is input

def loop():
	while True:
		if GPIO.input(PIR_OUT_PIN) == GPIO.LOW:
			print ('...Movement not detected!')
                time.sleep ( 1 )
		else:
			print ('Movement detected!...')

        
                dt_now = datetime.datetime.now()
                file_name = dt_now.strftime('%Y年%m月%d日%H時%M分%S秒')
                print (file_name)
        
                #カメラ映像を保存する
                cap = cv2.VideoCapture(0)
                fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                fps = 20.0
                size = (640, 360)
                writer = cv2.VideoWriter((file_name + '.m4v'), fmt, fps, size)
        
                i = 0
                #60フレーム撮影する
                while i < 60:
                    _, frame = cap.read()
                    frame = cv2.resize(frame, size)
                    writer.write(frame)
     
                    i = i + 1
             
                writer.release()
                cap.release()
        
                time.sleep( 10 )

def destroy():
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
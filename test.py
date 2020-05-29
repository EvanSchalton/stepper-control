
import RPi.GPIO as GPIO
from datetime import datetime
import time

def main():
	PINS = [7, 11, 13, 15]
	
	HALFSTEP_SEQ = [
		[1,0,0,0],
		[1,1,0,0],
		[0,1,0,0],
		[0,1,1,0],
		[0,0,1,0],
		[0,0,1,1],
		[0,0,0,1],
		[1,0,0,1],
	]
	
	Rotations = 1
	RPM = 100
	
	STEPS_PER_ROTATION = int(360/1.8)
	print("STEPS_PER_ROTATION:", STEPS_PER_ROTATION)
	delay = float(60/float(RPM*STEPS_PER_ROTATION))
	steps = int(STEPS_PER_ROTATION * Rotations)
	print("Delay:", delay)

	GPIO.setmode(GPIO.BOARD)
	
	for pin in PINS:
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, False)
	
	try:
		start_time = datetime.now()
		for i in range(steps):
			for halfstep in HALFSTEP_SEQ:
				for pin in range(4):
					GPIO.output(PINS[pin], halfstep[pin])
				#print(halfstep)
				time.sleep(delay)
		print("Runtime:", datetime.now()-start_time)
				
	except KeyboardInterrupt:
		print("Stopped by Ctrl+C")
		pass
	
	finally:
		GPIO.cleanup()
	

if __name__ == '__main__':
	main()


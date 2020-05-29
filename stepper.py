import time
import RPi.GPIO as GPIO
import atexit

class Stepper:

	CYCLE_STEPS = [
		[1,0,0,0],
		[1,1,0,0],
		[0,1,0,0],
		[0,1,1,0],
		[0,0,1,0],
		[0,0,1,1],
		[0,0,0,1],
		[1,0,0,1],
	]
	
	AIN1_INDEX = 0
	AIN2_INDEX = 1
	
	BIN1_INDEX = 2
	BIN2_INDEX = 3
	
	def __init__(self,
		AIN1_PIN=7, AIN2_PIN=11, BIN1_PIN=13, BIN2_PIN=15,
		rpm=50, step_angle=1.8
	):
		self.AIN1_PIN = AIN1_PIN
		self.AIN2_PIN = AIN2_PIN
		self.BIN1_PIN = BIN1_PIN
		self.BIN2_PIN = BIN2_PIN
		
		self.step_angle = step_angle
		
		self.cycle_phase = 0
		
		self.steps = (360 / step_angle)
		self.setSpeed(rpm)		
		
		GPIO.setmode(GPIO.BOARD)
		for pin in [AIN1_PIN, AIN2_PIN, BIN1_PIN, BIN2_PIN]:
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, False)
		
	def setSpeed(self, rpm):
		"""Calculates the step delay to accomplish a given RPM"""
		self.step_delay = 60.0 / (self.steps * rpm)
		print("step delay", self.step_delay)
	
	@property
	def setPhase(self):
		"""Sets the signal for the motors pins based on half-step"""
		current_phase = self.CYCLE_STEPS[self.cycle_phase]
		#print("current_phase", current_phase)
		GPIO.output(self.AIN1_PIN, current_phase[self.AIN1_INDEX])
		GPIO.output(self.AIN2_PIN, current_phase[self.AIN2_INDEX])
		GPIO.output(self.BIN1_PIN, current_phase[self.BIN1_INDEX])
		GPIO.output(self.BIN2_PIN, current_phase[self.BIN2_INDEX])

	def oneStep(self, direction="CW"):
		"""Iterates the cycle phase based on direction"""
		direction_sign = 1
		if direction == "CCW":
			direction_sign = -1
		
		self.cycle_phase = (self.cycle_phase+direction_sign) % len(self.CYCLE_STEPS)
		self.setPhase
	
	@property
	def stepDelay(self):
		"""Sleeps for the required step delay"""
		time.sleep(self.step_delay)
	
	def step(self, steps, direction="CW"):
		"""Phases the motor throught the given step count in the given direction"""
		for current_step in range(steps):
			self.oneStep(direction=direction)
			self.stepDelay
	
	def rotate(self, angle):
		"""Rotates the motor based on a provided angle"""
		direction = "CW"
		if angle<0:
			direction = "CCW"
			
		steps = int(abs(angle)/self.step_angle)
		print("Rotate steps:", steps)
		
		self.step(steps, direction)
		
	def revolve(self, revolutions):
		"""Rotates the motor based on a provided number of revolutions"""
		self.rotate(360*revolutions)	
	
	@atexit.register
	def cleanup():
		"""Removes GPIO References"""
		print("Cleaning Up GPIO")
		GPIO.cleanup()
		





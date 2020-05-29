from stepper import Stepper
import itertools

RPM = 150
if False:
	pins = (13, 11, 12, 15)

	for index, pinConfig in enumerate(itertools.permutations(pins)):
		print(index, pinConfig)
		pin1 = pinConfig[0]
		pin2 = pinConfig[1]
		pin3 = pinConfig[2]
		pin4 = pinConfig[3]
		
		test = Stepper(pin1, pin2, pin3, pin4, RPM)
		#test.step_delay = .0001
		try:
			while True:
				test.oneStep()
				test.stepDelay
		except KeyboardInterrupt:
			done = raw_input("Select (Y/n):")
			print("DONE:", done)
			if done == "":
				pass
			else:
				print("SELECTED:", index, pinConfig)
				break
else:
	test = Stepper(13, 11, 12, 15, RPM)
	#test.step_delay = .001
	test.revolve(int(input("revolutions: ")))

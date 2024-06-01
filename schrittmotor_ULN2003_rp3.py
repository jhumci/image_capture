# https://ben.akrin.com/driving-a-28byj-48-stepper-motor-uln2003-driver-with-a-raspberry-pi/
#!/usr/bin/python3
import RPi.GPIO as GPIO


class StepperMotor:

    def __init__(self, in1 = 17, in2 = 18, in3 = 27, in4 = 22):
        
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4

        # careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
        self.step_sleep = 0.002

        self.step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°

        self.direction = False # True for clockwise, False for counter-clockwise

        # defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
        self.step_sequence = [[1,0,0,1],
                        [1,0,0,0],
                        [1,1,0,0],
                        [0,1,0,0],
                        [0,1,1,0],
                        [0,0,1,0],
                        [0,0,1,1],
                        [0,0,0,1]]

        # setting up
        GPIO.setmode( GPIO.BCM )
        GPIO.setup( in1, GPIO.OUT )
        GPIO.setup( in2, GPIO.OUT )
        GPIO.setup( in3, GPIO.OUT )
        GPIO.setup( in4, GPIO.OUT )

        # initializing
        GPIO.output( in1, GPIO.LOW )
        GPIO.output( in2, GPIO.LOW )
        GPIO.output( in3, GPIO.LOW )
        GPIO.output( in4, GPIO.LOW )

        self.motor_pins = [in1,in2,in3,in4]
        self.motor_step_counter = 0


    # Motor aktivieren und halten
    def enable_motor(self):
        pass

    # Motor freigeben
    def disable_motor(self):
        GPIO.output(self.in1, GPIO.LOW )
        GPIO.output(self.in2, GPIO.LOW )
        GPIO.output(self.in3, GPIO.LOW )
        GPIO.output(self.in4, GPIO.LOW )
        GPIO.cleanup()

    # Richtung setzen
    def set_direction(self, direction):
        if direction == 'left':
            self.direction = False # True for clockwise, False for counter-clockwise
        else:
            self.direction = True

    # Schritte ausführen

    def move(self, steps):
        
        for _ in range(steps):
            for pin in range(0, len(self.motor_pins)):
                GPIO.output(self.motor_pins[pin], self.step_sequence[motor_step_counter][pin] )
            if self.direction==True:
                motor_step_counter = (motor_step_counter - 1) % 8
            elif self.direction==False:
                motor_step_counter = (motor_step_counter + 1) % 8

    def move_by_degree(self, degree):
        steps = int(degree / 1.8)
        self.move(steps)


if __name__ == "__main__":
    stepper = StepperMotor()
    stepper.enable_motor()
    stepper.set_direction('left')
    stepper.move_by_degree(90)
    stepper.disable_motor()
    GPIO.cleanup()

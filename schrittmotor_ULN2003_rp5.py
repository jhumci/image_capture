#!/usr/bin/python3
import gpiod
import time

from gpiod.line import Direction, Value

class StepperMotor:

    @staticmethod
    def release():
        chip = gpiod.Chip('/dev/gpiochip4')
        chip.close()

    def __init__(self, in1=17, in2=18, in3=27, in4=22):
        
        StepperMotor.release()
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4

        self.step_sleep = 0.002
        self.step_count = 4096  # 5.625*(1/64) per step, 4096 steps is 360°

        self.direction = False  # True for clockwise, False for counter-clockwise

        self.step_sequence = [[1,0,0,1],
                        [1,0,0,0],
                        [1,1,0,0],
                        [0,1,0,0],
                        [0,1,1,0],
                        [0,0,1,0],
                        [0,0,1,1],
                        [0,0,0,1]]

        # Create LineSettings object with output direction
        line_settings = gpiod.LineSettings()
        line_settings.direction = Direction.OUTPUT

        self.chip = gpiod.Chip('/dev/gpiochip4')
        self.lines = self.chip.request_lines(
            consumer="StepperMotor",
            config={tuple([self.in1, self.in2, self.in3, self.in4]): line_settings}
        )

        self.motor_pins = [in1, in2, in3, in4]
        self.motor_step_counter = 0

        self.steps_taken = 0

    def enable_motor(self):
        pass

    def disable_motor(self):
        self.lines.set_values({
            self.in1: Value(0),
            self.in2: Value(0),
            self.in3: Value(0),
            self.in4: Value(0)
        })
        self.lines.release()

    def set_direction(self, direction):
        if direction == 'left':
            self.direction = False
        else:
            self.direction = True

    def move(self, steps):
        for _ in range(steps):
            values = {pin: Value(val) for pin, val in zip(self.motor_pins, self.step_sequence[self.motor_step_counter])}
            self.lines.set_values(values)
            time.sleep(self.step_sleep)

            if self.direction:
                self.motor_step_counter = (self.motor_step_counter - 1) % 8
            else:
                self.motor_step_counter = (self.motor_step_counter + 1) % 8

        self.steps_taken += steps if not self.direction else -steps

    def move_by_degree(self, degree):
        steps = int(4096*(degree / 360))
        self.move(steps)

    def move_to_original_position(self):
        original_direction = self.direction
        self.set_direction('right' if self.steps_taken > 0 else 'left')
        self.move(abs(self.steps_taken))
        self.set_direction('left' if original_direction else 'right')

if __name__ == "__main__":
    stepper = StepperMotor()
    stepper.enable_motor()
    stepper.set_direction('left')
    stepper.move_by_degree(360)
    #stepper.move_to_original_position()
    stepper.disable_motor()

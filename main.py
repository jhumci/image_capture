import config
import time
import schrittmotor
import camera

# In Start State Verbinde Kamera und lies config aus

if __name__ == "__main__":
    
    # Connect Camera
    cam = camera.Camera()
    # Move to start position
    stepper = schrittmotor.StepperMotor()

    # For Position 

    positions = range(0,360-1,int(360/config.number_of_images))

    for position in positions:

        print(position)
        
        stepper.move_by_degree(position)

        # Make a Picture and store it based on time and position
        cam.set_file_path(config.output_directory)
        cam.set_file_name(f"{time.time()}_{position}_captured_image.jpg")

        # Make prediction based on the picture

    # move to start position

    stepper.move_by_degree(360-max(positions))

    
    
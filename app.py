import streamlit as st
import os
import config
from transformations import canny_edge_detection
import camera
import time
from schrittmotor_ULN2003_rp5 import StepperMotor

StepperMotor.release()

stepper = StepperMotor()
stepper.set_direction('left')



path = config.output_directory

st.title('Image Analysis')

# make two columns one for the original image and one for the transformed image


tab1, tab2, tab3 = st.tabs(["Image Capture", "Edge Detection", "AI"])

with tab1:

# Set the number of images to capture

    st.write("## Test Image")
    if st.button("Make Test Image"):
        cam = camera.Camera()
        cam.set_file_path("./test_images")
        cam.set_file_name(f"{int(time.time())}_captured_image.CR2")
        test_image = cam.capture_image()
        st.image(test_image)


    st.write("## Image Series")
    number_of_images = st.number_input("Number of Images to Capture", 1, 10, 1)

    
    # make an input field fir comments
    name = st.text_input("Name for the Folder")

    comments = st.text_area("Comments")

    if st.button("Capture Images!"):
        cam = camera.Camera()
        cam.set_file_path(f"./{name}")

        degree_step = 360/number_of_images
        degree = 0
        for position in range(0,number_of_images):
            stepper.move_by_degree(degree_step)
            degree = degree + degree_step
            time.sleep(0.5)
            #image_folder = "./test_images"
            image_folder = "./captured_images/" + name
            
            cam.set_file_path(image_folder)
            cam.set_file_name(f"{int(time.time())}_{str(int(degree))}_captured_image.CR2")
            test_image = cam.capture_image()
        
            st.write(f"## Image Captured Last at {degree} degree")
            st.image(test_image)

        # Show a list of the captured images
        st.write("## Captured Images")
        images = [f.name for f in os.scandir(image_folder) if f.is_file()]
        st.write(images)

        stepper.disable_motor()

    st.write("## Motor Options")

    degree = st.number_input("Turn Motor by degree")

    if st.button("Turn motor by degree!"):
        stepper.move_by_degree(int(degree))

    if st.button("Bring back to original position"):
        stepper.move_to_original_position()
    
"""    if st.button("Set motor back to zero!"):
        stepper.disable_motor()
        stepper = StepperMotor()
        stepper.set_direction('left')

    st.write("Steps taken: ", stepper.steps_taken)"""

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.write("## Original Image")

        # show subfolders to select

        subfolders = [f.name for f in os.scandir(path) if f.is_dir()]

        selected_subfolder = st.selectbox("Select a subfolder", subfolders)

        # show images in the selected subfolder

        images = [f.name for f in os.scandir(f"{path}/{selected_subfolder}") if f.is_file()]

        selected_image = st.selectbox("Select an image", images)

        # show the selected image

        

    with col2:


        st.write("## Select Parameters")

        # make sliders for the parameters

        low_threshold = st.slider("Low Threshold", 0, 255, 150)
        high_threshold = st.slider("High Threshold", 0, 255, 160)
        apertureSize = st.slider("Aperture Size", 3, 7, 3, step=2)


        transformed_image = canny_edge_detection(f"{path}/{selected_subfolder}/{selected_image}", low_threshold, high_threshold, apertureSize)

        

    col3, col4 = st.columns(2)

    with col3:
        st.image(f"{path}/{selected_subfolder}/{selected_image}")

    with col4:
        st.image(transformed_image)
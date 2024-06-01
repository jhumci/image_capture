import cv2
import os
import numpy as np
import config


def canny_edge_detection(fitem, low_threshold, high_threshold, apertureSize=3):

    image = cv2.imread(fitem)
    # Grayscale conversion
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Canny edge detection
    edges = cv2.Canny(gray, low_threshold, high_threshold, apertureSize=apertureSize)
    
    # Define the output file path
    fout = os.path.join(config.output_directory, "canny_"+ fitem)

    # if fout ends with CR2, replace it with jpg
    if fout.endswith(".CR2"):
        fout = fout.replace(".CR2", ".jpg")
        
    # Save the grayscale image with detected edges
    cv2.imwrite(fout, edges)
    return edges


if __name__ == "__main__":
    # Get the current working directory
    path = "captured_images"

    # Define input and output directories
    inputPar = os.path.join(path)
    outPar = os.path.join(path, 'Output')
    os.makedirs(outPar, exist_ok=True)

    # List all files in the input directory
    files = os.listdir(inputPar)

    # Loop through each file in the input directory
    for file in files:
        fitem = os.path.join(inputPar, file)
        image = cv2.imread(fitem)

        # Grayscale conversion
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #print(gray)

        # Canny edge detection
        edges = cv2.Canny(gray, 150, 160, apertureSize=3)
        print(edges)

        """
        # Hough Line Transform
        lines = cv2.HoughLines(edges, 1.5, np.pi / 180, 200)

        # Iterate through each detected line
        for line in lines:
            rho, theta = line[0]
            # Convert polar coordinates to Cartesian coordinates
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            # Draw lines on the original image
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

        """
        # Define the output file path
        fout = os.path.join(outPar, file)

        # Save the grayscale image with detected edges
        cv2.imwrite(fout, edges)
import cv2
import os
from PIL import Image
import numpy as np 


def process_image(image, crop_ratios=(0.35, 0.65), new_width=500):
    """
    Crops, resizes, and saves an image.

    Parameters:
    - image as a pip
    - crop_ratios (tuple): Tuple with left and right crop ratios (default=(0.3, 0.7)).
    - new_width (int): Desired width of the output image while maintaining aspect ratio.
    """
    # Crop the image
    width, height = image.size


    # Resize the image
    aspect_ratio = height/ width
    new_height = int(new_width * aspect_ratio)
    return(image.resize((new_width, new_height)))

def extract_frames(video_path, output_folder1,output_folder2):
    """
    Extracts frames from a video and saves them as images in the specified folder.

    Parameters:
    - video_path (str): Path to the video file.
    - output_folder (str): Path to the folder where frames will be saved.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder1):
        os.makedirs(output_folder1)

    if not os.path.exists(output_folder2):
        os.makedirs(output_folder2)

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print("Error: Could not open video.")
        return

    frame_number = 0
    # we can make code better here by actaully changing the amounts we want to put to test and tran
    test = 31
    train = 103
    while True:
        success, frame = video_capture.read()
        
        if not success:
            break  # Exit when there are no more frames
      

       
        # Save the frame as an image
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        processed_pil_image = process_image(pil_image)
        processed_frame = cv2.cvtColor(np.array(processed_pil_image), cv2.COLOR_RGB2BGR)
        if frame_number < test:
            frame_filename = os.path.join(output_folder1, f"frame_{frame_number:04d}.jpg")
            cv2.imwrite(frame_filename, processed_frame)
            print(f"Saved {frame_filename}")
        elif frame_number < train:
            frame_filename2 = os.path.join(output_folder2, f"frame_{frame_number:04d}.jpg")
            cv2.imwrite(frame_filename2, processed_frame)
            print(f"Saved {frame_filename2}")
        else:
            break
        frame_number += 1

    # Release the video capture
    video_capture.release()
    print("Frame extraction complete.")

# Example usage
def main():
    video_path = r"C:\Users\leoca\Downloads\Photos-001\IMG_1749.MOV" # Use raw string
    output_folder = "A"  # Replace with your desired output folder
    output_folder2 = "A_"
    extract_frames(video_path, output_folder,output_folder2)
    

"""
    input_path = "path_to_your_input_image.jpg"  # Replace with your input image path
    output_path = "processed_image.jpeg"         # Replace with desired output path
    

"""
main()
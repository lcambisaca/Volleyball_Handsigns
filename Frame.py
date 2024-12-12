import cv2
import os
from PIL import Image
import numpy as np 
import random
import shutil

def shuffle_and_split(source_folder, output_folder1, output_folder2, split_ratio=0.8):
    # Create output folders if they don't exist
    if not os.path.exists(output_folder1):
        os.makedirs(output_folder1)
    if not os.path.exists(output_folder2):
        os.makedirs(output_folder2)

    # List all files in the source folder
    files = os.listdir(source_folder)

    # Shuffle the files
    random.shuffle(files)
   

    # Split files based on the ratio
    split_point = int(len(files) * split_ratio)
    files_for_folder1 = files[:split_point]
    files_for_folder2 = files[split_point:]
    random.shuffle(files_for_folder1)
    random.shuffle(files_for_folder2)

    # Move files to the respective folders
    for file in files_for_folder1:
        shutil.move(os.path.join(source_folder, file), os.path.join(output_folder1, file))

    for file in files_for_folder2:
        shutil.move(os.path.join(source_folder, file), os.path.join(output_folder2, file))

    print(f"Moved {len(files_for_folder1)} files to {output_folder1}.")
    print(f"Moved {len(files_for_folder2)} files to {output_folder2}.")


def process_image(image, new_height=64):
 
    # Crop the image
    width, height = image.size
    # Resize the image
    aspect_ratio =  width/height
    new_width = int(new_height * aspect_ratio)
    return(image.resize((new_width, new_height)))

def extract_frames(video_path,output_folder):
    """
    Extracts frames from a video and saves them as images in the specified folder.

    Parameters:
    - video_path (str): Path to the video file.
    - output_folder (str): Path to the 1st_folder where frames will be saved.
    """
   

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print("Error: Could not open video.")
        return
    

    total_frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_number = 0
    Max = 200 # * The total amount of pics you want
    every_frame = 3 # * This makes it so every n frames we take a screenshot of the video 
    curr_shot = 0 
    print(every_frame)
   
    while True:
        success, frame = video_capture.read()
        if not success:
            break  # Exit when there are no more frames
        if frame_number % every_frame == 0:
            # Save the frame as an image
            if curr_shot > Max:
                break
            pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            processed_pil_image = process_image(pil_image)
            processed_frame = cv2.cvtColor(np.array(processed_pil_image), cv2.COLOR_RGB2BGR)
            frame_filename = os.path.join(output_folder, f"frame_{curr_shot:04d}.jpg")
            cv2.imwrite(frame_filename, processed_frame)
            print(f"Saved {frame_filename}")
            curr_shot +=1
        frame_number += 1

    # Release the video capture
    video_capture.release()
    
    print("Frame extraction complete.")
    

# Example usage
def main():

    video_path = r"C:\Users\leoca\Downloads\4 - Made with Clipchamp.mp4" # Change to w.e image
    frame_folder = "Frames"
    output1 = "4"  # Replace with your desired output folder
    output2 = "4_"
    extract_frames(video_path, frame_folder)
    # Example usage
    shuffle_and_split(frame_folder, output1, output2, split_ratio=0.8)

main()

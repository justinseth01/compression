"""
compression.py

This program is an image compression tool that compresses
the image everywhere except for the facial features recognized
in each photo.  I got the inspiration to make this from instagram 
because I would zoom in on photos only to see the photo was
compressed so much that it was hard to see my friends' faces.
Based on my testing, there was an average of ~15% size difference
between the fully compressed photo and the facial sensitive version.

This program accepts images from the "images" directory and
outputs them into the output_images directory.  A "temp" folder
is created for the intermediate step of creating a fully compressed
photo first before superimposing the non-compressed facial areas.

Uncomment line 64 to see faces outlined by a square
Change jpeg_quality = 5 for more dramatic results (line 49)

Justin Seth
8/15/2023
"""

import cv2
import os
import shutil

def background_compression(image_path,image_name):
    # Create output_images folder if doesn't already exist
    if not os.path.exists("output_images"):
        os.mkdir("output_images")

    output_path = "output_images"

    # Load the image
    image_path = image_path + os.path.sep + image_name
    image = cv2.imread(image_path)
    
    # Load the pre-trained Haarcascades classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Convert the image to grayscale for face detection
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Define jpeg quality (~90 is standard but 10 is used to show more noticable results)
    jpeg_quality = 10  # A value between 0 and 100 (higher means better quality, but larger file size)

    # Compress original image and save to temp
    temp_path = "temp"+os.path.sep+image_name
    cv2.imwrite(temp_path, image, [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality])

    # Load compressed image into variable
    image2 = cv2.imread(temp_path)
    
    # Superimpose non-compressed faces onto compressed image
    for (x, y, w, h) in faces:
        face_roi = image[y:y+h, x:x+w]
        image2[y:y+h, x:x+w] = face_roi

        # # uncomment to see detected faces
        # cv2.rectangle(image2, (x, y), (x+w, y+h)4, (255, 0, 0), 2)
    
    # Output new image
    cv2.imwrite(output_path+os.path.sep+image_name, image2)

    print("Compressed "+image_name)


def analysis():
    # Analysis of percent difference between facially compressed image
    # and standard compression relative to original image size

    percent_diff = []

    for image_name in os.listdir("output_images"):
        # Get image size and convert to megabytes
        original_size = os.path.getsize("images" + os.path.sep + image_name)*pow(10,-6)
        output_size = os.path.getsize("output_images" + os.path.sep + image_name)*pow(10,-6)
        compressed_size = os.path.getsize("temp" + os.path.sep + image_name)*pow(10,-6)

        # Calculate percent difference
        percent_diff_compressed = 100*(compressed_size-original_size)/original_size
        percent_diff_output = 100*(output_size-original_size)/original_size

        # # Uncomment to see percentage difference in size
        # # in comparison to the original picture file
        # print(image_name)
        # print("compressed percent diff: "+ str(round(percent_diff_compressed,1)))
        # print("output percent diff: "+ str(round(percent_diff_output,1)))
        # print()

        percent_diff.append((image_name, percent_diff_compressed-percent_diff_output))

    print()
    print("percent diff values:")
    for value in percent_diff:
        print(value[0])
        print("Percent diff: "+str(round(value[1],1)))
        print()


if __name__ == "__main__":
    # Remove any old temp directory if not previously deleted
    if os.path.exists("temp"):
        shutil.rmtree("temp")

    # Make temp directory for storing intermediate images
    os.mkdir("temp")

    image_path = "images"  # Image path

    # Iterate through all images in image_path
    for image in os.listdir(image_path):
        background_compression(image_path,image)

    # Uncomment to analyze percent differences between partially and fully compressed images
    # analysis()
    
    # Comment out if you want to view the fully compressed photos
    if os.path.exists("temp"):
        shutil.rmtree("temp")

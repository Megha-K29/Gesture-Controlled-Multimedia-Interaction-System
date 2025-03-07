
## This code is used to blur the text in the top left side and the top right side of each images.

import cv2
import os

def blur_areas_in_images(image_dir, top_left_coords, top_right_coords, output_dir, blur_radius=(31, 31)):
    # Get a list of all image files in the directory
    image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]

    for image_path in image_paths:
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error loading image {image_path}")
            continue

        # Blur the top left area
        x1, y1, x2, y2 = top_left_coords  
        image[y1:y2, x1:x2] = cv2.GaussianBlur(image[y1:y2, x1:x2], blur_radius, 0)

        # Blur the top right area
        x1, y1, x2, y2 = top_right_coords
        image[y1:y2, x1:x2] = cv2.GaussianBlur(image[y1:y2, x1:x2], blur_radius, 0)

        # Save the blurred image
        output_path = os.path.join(output_dir, os.path.basename(image_path))
        cv2.imwrite(output_path, image)

# Example usage
image_dir = r"C:\Users\user\Desktop\editings\images"  # Directory containing images
output_dir = r"C:\Users\user\Desktop\editings\blurred images"  # Directory to save blurred images
os.makedirs(output_dir, exist_ok=True)

# Coordinates for blurring
top_left_coords = (3, 54, 452, 97)  # (x1, y1, x2, y2) 
top_right_coords = (1649, 50, 1796, 97)  # (x1, y1, x2, y2)

blur_areas_in_images(image_dir, top_left_coords, top_right_coords, output_dir)




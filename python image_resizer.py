from PIL import Image
import io
import os

def resize_image(input_image_path, target_size_kb, output_image_path):
    """
    Resizes the image to meet the target size in KB by adjusting the quality.
    """
    original_image = Image.open(input_image_path)
    
    # Initialize parameters
    quality = 90  # Start with high quality
    step = 5  # Quality adjustment step
    attempt_count = 0
    max_attempts = 30

    # Function to calculate image size in KB
    def get_image_size_in_kb(image, quality):
        # Save image to memory buffer
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=quality)
        return len(img_byte_arr.getvalue()) / 1024  # Return size in KB
    
    # Try to resize until the target size is achieved
    while attempt_count < max_attempts:
        # Save the image with the current quality
        img_byte_arr = io.BytesIO()
        original_image.save(img_byte_arr, format='JPEG', quality=quality)
        
        # Calculate the current image size in KB
        current_size_kb = get_image_size_in_kb(original_image, quality)
        print(f"Attempt {attempt_count + 1}: Size = {current_size_kb:.2f} KB at quality = {quality}")

        # Check if we are within the acceptable range (±1 KB)
        if current_size_kb > target_size_kb + 1:
            quality -= step  # Decrease quality to reduce size
        elif current_size_kb < target_size_kb - 1:
            quality += step  # Increase quality to enlarge the image
        else:
            # Save the final image if the size is within range
            with open(output_image_path, 'wb') as f:
                f.write(img_byte_arr.getvalue())
            print(f"Image resized successfully: {current_size_kb:.2f} KB")
            return output_image_path  # Return path to the resized image
        
        attempt_count += 1
    
    print("Unable to achieve the exact target size.")
    return None

def main():
    input_image_path = input("Enter the path to the image you want to resize: ")
    target_size_kb = int(input("Enter the target size in KB (e.g., 300): "))
    output_image_path = "resized_image.jpg"  # Output file path for the resized image
    
    # Resize the image and get the resized image file path
    resized_image = resize_image(input_image_path, target_size_kb, output_image_path)
    
    if resized_image:
        print(f"Resized image saved at: {resized_image}")
    else:
        print("Failed to resize the image to the target size.")

if __name__ == "__main__":
    main()

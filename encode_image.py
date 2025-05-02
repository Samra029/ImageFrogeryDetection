import cv2
import os

def encrypt():
    # Folder and file paths
    base_path = 'Screenshot'
    img1_path = os.path.join(base_path, '1.jpg')
    img2_path = os.path.join(base_path, '2.jpg')

    # Read the images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    # Error check
    if img1 is None:
        print(f"❌ Error: Couldn't load {img1_path}")
        return
    if img2 is None:
        print(f"❌ Error: Couldn't load {img2_path}")
        return

    # Resize img2 to match img1 if needed
    if img1.shape != img2.shape:
        print("⚠️ Warning: Image sizes differ. Resizing img2 to match img1...")
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Create a copy of img1 to store the result
    result = img1.copy()

    # Encode image: merge 4 MSBs of img1 and 4 MSBs of img2
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            for c in range(3):  # For each channel (BGR)
                v1 = format(img1[i, j, c], '08b')  # Pixel from img1
                v2 = format(img2[i, j, c], '08b')  # Pixel from img2
                merged = v1[:4] + v2[:4]           # First 4 bits of each
                result[i, j, c] = int(merged, 2)

    # Save encoded image
    output_path = '3.png'
    cv2.imwrite(output_path, result)
    print(f"✅ Encoding complete! Output saved as {output_path}")

# Run the encryption
if __name__ == "__main__":
    encrypt()

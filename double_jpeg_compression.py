import os
import numpy as np
import cv2
from scipy import fftpack as fftp
from matplotlib import pyplot as plt

def detect(image):
    firstq = 30
    secondq = 40
    thres = 0.5

    dct_rows = 0
    dct_cols = 0

    image = cv2.imread(image)
    if image is None:
        raise ValueError("Image not found or invalid path.")
    
    shape = image.shape

    if shape[0] % 8 != 0:
        dct_rows = shape[0] + 8 - shape[0] % 8
    else:
        dct_rows = shape[0]

    if shape[1] % 8 != 0:
        dct_cols = shape[1] + 8 - shape[1] % 8
    else:
        dct_cols = shape[1]

    dct_image = np.zeros((dct_rows, dct_cols, 3), np.uint8)
    dct_image[0:shape[0], 0:shape[1]] = image

    y = cv2.cvtColor(dct_image, cv2.COLOR_BGR2YCR_CB)[:, :, 0]

    w = y.shape[1]
    h = y.shape[0]
    n = w * h / 64

    Y = y.reshape(h // 8, 8, -1, 8).swapaxes(1, 2).reshape(-1, 8, 8)

    qDCT = []

    for i in range(0, Y.shape[0]):
        qDCT.append(cv2.dct(np.float32(Y[i])))

    qDCT = np.asarray(qDCT, dtype=np.float32)
    qDCT = np.rint(qDCT - np.mean(qDCT, axis=0)).astype(np.int32)

    f, a1 = plt.subplots(8, 8)
    a1 = a1.ravel()

    k = 0
    for idx, ax in enumerate(a1):
        k += 1
        data = qDCT[:, int(idx / 8), int(idx % 8)]
        val, key = np.histogram(data, bins=np.arange(data.min(), data.max() + 1))
        
        # Compute the FFT of the histogram
        z = np.absolute(fftp.fft(val))
        z = np.reshape(z, (len(z), 1))
        rotz = np.roll(z, int(len(z) / 2))

        # Detect peaks in the FFT spectrum
        slope = rotz[1:] - rotz[:-1]
        indices = [i + 1 for i in range(len(slope) - 1)
                   if slope[i] > 0 and slope[i + 1] < 0]

        peak_count = 0

        # Count peaks above the threshold
        for j in indices:
            if rotz[j][0] > thres:
                peak_count += 1

        if k == 3:
            if peak_count >= 20:
                return True
            else:
                return False

# Function to process all images in a folder
def process_images_from_folder(folder_path):
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        if image_name.endswith(".jpg") or image_name.endswith(".jpeg"):
            print(f"Testing image: {image_name}")
            result = detect(image_path)
            if result:
                print(f"✅ Double JPEG compression detected in {image_name}.")
            else:
                print(f"❌ No double JPEG compression detected in {image_name}.")

if __name__ == "__main__":
    # Path to your 'Compression Detection' folder
    compression_detection_folder_path = "D:/Image_Manipulation_Detection_System_Python-main/input/Compression Detection"
    process_images_from_folder(compression_detection_folder_path)

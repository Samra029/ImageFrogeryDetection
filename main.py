import sys
import cv2
from ForgeryDetection import Detect
import re
from datetime import datetime
import os.path as path
from PIL import Image, ExifTags
import double_jpeg_compression
import noise_variance
from optparse import OptionParser

def PrintBoundary():
    print('*' * 50)

def main():
    # Command line options
    cmd = OptionParser("usage: %prog image_file [options]")
    cmd.add_option('', '--imauto', help='Automatically search identical regions.', default=1)
    cmd.add_option('', '--imblev', help='Blur level for degrading image details.', default=8)
    cmd.add_option('', '--impalred', help='Image palette reduction factor.', default=15)
    cmd.add_option('', '--rgsim', help='Region similarity threshold.', default=5)
    cmd.add_option('', '--rgsize', help='Region size threshold.', default=1.5)
    cmd.add_option('', '--blsim', help='Block similarity threshold.', default=200)
    cmd.add_option('', '--blcoldev', help='Block color deviation threshold.', default=0.2)
    cmd.add_option('', '--blint', help='Block intersection threshold.', default=0.2)
    
    opt, args = cmd.parse_args()
    if not args:
        cmd.print_help()
        sys.exit(1)

    file_name = sys.argv[1]
    input_path = path.join('input', file_name)
    
    if not path.exists(input_path):
        sys.exit(f"Image not found: {input_path}. Please place the image in the input subdirectory.")

    # 1. Double JPEG compression detection
    PrintBoundary()
    print('\nRunning double JPEG compression detection...')
    try:
        double_compressed = double_jpeg_compression.detect(input_path)
        print('\nDouble compression detected' if double_compressed else '\nSingle compressed')
    except Exception as e:
        print(f"\nError in double JPEG compression detection: {str(e)}")
    PrintBoundary()

    # 2. Metadata analysis
    PrintBoundary()
    print('\nRunning Metadata Analysis detection')
    try:
        with Image.open(input_path) as img:
            img_exif = img.getexif()
            if img_exif is None:
                print('No EXIF data found.')
            else:
                for key, val in img_exif.items():
                    if key in ExifTags.TAGS:
                        print(f'{ExifTags.TAGS[key]}: {val}')
    except Exception as e:
        print(f"Error in metadata analysis: {str(e)}")
    PrintBoundary()

    # 3. Noise variance inconsistency detection
    PrintBoundary()
    print('\nRunning noise variance inconsistency detection...')
    try:
        noise_forgery = noise_variance.detect(input_path)
        print('\nNoise variance inconsistency detected' if noise_forgery 
              else '\nNo noise variance inconsistency detected')
    except Exception as e:
        print(f"\nError in noise variance detection: {str(e)}")
    PrintBoundary()

    # 4. Copy-Move detection
    PrintBoundary()
    print('\nRunning Copy-Move Forgery Detection')
    
    # Get parameters from command line or use defaults
    eps = 60
    min_samples = 2
    
    if len(sys.argv) > 2:
        try:
            eps = int(sys.argv[2])
            if not (0 < eps <= 500):
                print('Eps value out of range (0,500], using default 60')
                eps = 60
        except ValueError:
            print('Invalid eps value, using default 60')
    
    if len(sys.argv) > 3:
        try:
            min_samples = int(sys.argv[3])
            if not (0 < min_samples <= 50):
                print('min_samples value out of range (0,50], using default 2')
                min_samples = 2
        except ValueError:
            print('Invalid min_samples value, using default 2')
    
    print(f'\nParameters: eps={eps}, min_samples={min_samples}')
    
    try:
        detect = Detect(input_path)
        key_points, descriptors = detect.siftDetector()
        
        if not key_points:
            print('\nNo keypoints detected - cannot perform copy-move detection')
        else:
            forgery = detect.locateForgery(eps, min_samples)
            
            if forgery is not None:
                cv2.imshow('Original image', detect.image)
                cv2.imshow('Forgery Detection Result', forgery)
                
                print("\nPress 's' to save result or 'q' to quit")
                while True:
                    key = cv2.waitKey(100) & 0xFF
                    if key == ord('q'):
                        break
                    elif key == ord('s'):
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        output_name = f"{path.splitext(file_name)[0]}_forgery_{timestamp}.jpg"
                        cv2.imwrite(output_name, forgery)
                        print(f"Result saved as: {output_name}")
                        break
                
                cv2.destroyAllWindows()
            else:
                print('\nNo copy-move forgery detected')
    except Exception as e:
        print(f'\nError in copy-move detection: {str(e)}')
    
    PrintBoundary()

if __name__ == "__main__":
    main()
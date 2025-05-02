import os

# Ensure script runs from the project folder
os.chdir("D:/Image_Manipulation_Detection_System_Python-main")

message = "iss baar Paper presentation bhi karna hai"
image_path = "input\Copy-Move\forged2.jpg"
output_path = "temp.jpg"

try:
    with open(image_path, "rb") as img_file:
        image_data = img_file.read()

    with open(output_path, "wb") as out_file:
        out_file.write(image_data)
        out_file.write(b"\n")
        out_file.write(message.encode('utf-8'))

    print(f"✅ Message successfully embedded into {output_path}")

except FileNotFoundError:
    print("❌ Error: Image file not found. Check the path.")
except Exception as e:
    print(f"❌ An error occurred: {e}")

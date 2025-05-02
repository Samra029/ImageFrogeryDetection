import os
import binascii
from tkinter import *
from prettytable import PrettyTable

filename = os.path.join('Screenshot', '2.jpg')  # ✅ Corrected path

# Check if file exists
if not os.path.exists(filename):
    print(f"Error: {filename} not found.")
else:
    # Create Tkinter window
    master = Tk()
    master.title("Hex Viewer")

    # Create PrettyTable instance
    t = Text(master, wrap=NONE)
    x = PrettyTable()
    x.field_names = ["Bytes", "8-bit", "String"]

    with open(filename, "rb") as f:
        n = 0
        b = f.read(16)

        while b:
            s1 = " ".join([f"{i:02x}" for i in b])  # Hex string
            s1 = s1[0:23] + " " + s1[23:]  # Add extra space for readability

            # ASCII string
            s2 = "".join([chr(i) if 32 <= i <= 127 else "." for i in b])

            x.add_row([f"{n * 16:08x}", f"{s1:<48}", f"{s2}"])
            n += 1
            b = f.read(16)

        # Insert the table as text into Tkinter window
        t.insert(INSERT, x.get_string())
        t.config(state=DISABLED)
        t.pack()

        # Display file size
        label = Label(master, text=f"File Size: {os.path.getsize(filename):08x}")
        label.pack(pady=10)

    # Run Tkinter main loop
    master.mainloop()

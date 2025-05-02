import streamlit as st
from PIL import Image
import os

# --- Session state initialization ---
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None

if 'result_image' not in st.session_state:
    st.session_state.result_image = None

# --- App Title ---
st.title("📷 IMAGE FORGERY DETECTOR")

# --- Top Layout ---
col1, col2, col3 = st.columns([1, 2, 1])

# Input image (either default or uploaded)
with col1:
    if st.session_state.uploaded_image:
        st.image(st.session_state.uploaded_image, caption="INPUT IMAGE", width=150)
    else:
        st.image("images/input.png", caption="INPUT IMAGE", width=150)

# Center Instructions
with col2:
    st.subheader("IMAGE FORGERY DETECTION")
    with st.expander("📋 INSTRUCTIONS"):
        st.markdown("""
        1. Click **Upload Image**  
        2. Choose a **Forgery Method**  
        3. Wait a few seconds  
        4. See the **Output**
        """)

# Output image (either default or generated)
with col3:
    if st.session_state.result_image:
        st.image(st.session_state.result_image, caption="OUTPUT", width=150)
    else:
        st.image("images/output.png", caption="OUTPUT", width=150)

# --- File Upload ---
uploaded_file = st.file_uploader("📤 Upload Image", type=["jpg", "png", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.session_state.uploaded_image = image
    st.session_state.result_image = None  # reset output when new image is uploaded
    st.success("Image uploaded successfully!")

# --- Function to apply forgery detection methods ---
def apply_detection(method_name):
    if st.session_state.uploaded_image:
        img = st.session_state.uploaded_image.copy()

        # Example opt_value for passing additional parameters to functions
        opt_value = {'key1': 'value1', 'key2': 'value2'}  # Modify as needed for each method

        # Select method and apply detection
        if method_name == "Compression Detection":
            from double_jpeg_compression import detect  # Assuming this is your method
            result = detect(img, opt_value)  # Modify if needed
        elif method_name == "Noise Inconsistency":
            from noise_variance import detect_noise_inconsistency  # Assuming you have this method
            result = detect_noise_inconsistency(img)  # Pass opt_value here if required
        elif method_name == "Copy-Move":
            from ForgeryDetection import Detect  # Assuming your forgery detection script
            forgery_detector = Detect(img)
            result = forgery_detector.locateForgery()  # No opt_value needed here
        elif method_name == "Error Level Analysis":
            from ForgeryDetection import perform_ela  # Assuming this function is present
            result = perform_ela(img)  # Modify as per function signature

        # Check if result is valid
        if result is None:
            st.error("Detection failed. The result is None.")
            return

        # Ensure the 'results' directory exists
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Save the result image
        result_path = f"{results_dir}/{method_name.lower().replace(' ', '_')}_output.png"
        result.save(result_path)

        # Display the image result directly
        st.session_state.result_image = result

    else:
        st.warning("Please upload an image first!")

# --- Detection Methods ---
st.markdown("### 🧪 Select Forgery Detection Method:")
col4, col5, col6 = st.columns(3)

with col4:
    if st.button("Compression-Detection"):
        apply_detection("Compression Detection")
    if st.button("Metadata-Analysis"):
        apply_detection("Metadata Analysis")

with col5:
    if st.button("Noise-Inconsistency"):
        apply_detection("Noise Inconsistency")
    if st.button("Error-Level Analysis"):
        apply_detection("Error Level Analysis")

with col6:
    if st.button("Copy-Move"):
        apply_detection("Copy-Move")
    if st.button("Image-Extraction"):
        apply_detection("Image Extraction")

# Extra buttons
col_exit = st.columns(1)[0]
if col_exit.button("String Extraction"):
    apply_detection("String Extraction")

if col_exit.button("Exit program"):
    st.warning("You clicked exit. (This is just a placeholder in Streamlit)")

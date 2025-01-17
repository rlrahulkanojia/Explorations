import streamlit as st
import io
import os
import uuid
from PIL import Image
from service.inference.process import generate_mask, load_seg_model, get_palette
from service.commons.environment import CHECKPOINT_PATH, DEVICE, OUTPUT_DIR
from service.commons.logger import get_logger

# Initialize logging
log = get_logger(__name__)

@st.cache_resource
def load_model():
    """Load the model once and cache it"""
    model = load_seg_model(CHECKPOINT_PATH, device=DEVICE)
    palette = get_palette(4)
    return model, palette

def process_image(image, model, palette):
    """Process a single image with the model"""
    try:
        segmented_image = generate_mask(
            image,
            net=model,
            palette=palette,
            device=DEVICE
        )

        # Convert to RGB mode if needed
        if segmented_image.mode in ('RGBA', 'P'):
            segmented_image = segmented_image.convert('RGB')

        # Save the output
        filename = f"output_{uuid.uuid4()}.jpg"
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, filename)
        segmented_image.save(output_path, format="JPEG")

        return segmented_image, output_path
    except Exception as e:
        log.error(f"Error processing image: {str(e)}")
        raise e

def main():
    st.set_page_config(
        page_title="Cloth Segmentation Tool",
        page_icon="👕",
        layout="wide"
    )

    # Load model at startup
    with st.spinner("Loading model..."):
        model, palette = load_model()

    # Custom CSS
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .upload-box {
            border: 2px dashed #aaa;
            padding: 20px;
            text-align: center;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title and description
    st.title("👕 Cloth Segmentation Tool")
    st.markdown("""
    Upload an image of clothing to segment it and get different parts separated.
    The model will identify different components of the clothing item.
    """)

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file", 
        type=["jpg", "jpeg", "png"],
        help="Upload an image of clothing"
    )

    # Create columns for before/after display
    col1, col2 = st.columns(2)

    if uploaded_file is not None:
        try:
            # Display original image
            with col1:
                st.subheader("Original Image")
                image = Image.open(uploaded_file)
                st.image(image, use_container_width=True)
                
                # Display image metadata
                with st.expander("Image Details"):
                    st.write(f"Size: {image.size}")
                    st.write(f"Mode: {image.mode}")
                    st.write(f"Format: {image.format}")

            # Process image
            with st.spinner("Processing image..."):
                segmented_image, output_path = process_image(image, model, palette)
                
                # Display processed image
                with col2:
                    st.subheader("Segmented Result")
                    st.image(segmented_image, use_container_width=True)
                    
                    # Download button
                    with open(output_path, "rb") as file:
                        btn = st.download_button(
                            label="Download Segmented Image",
                            data=file,
                            file_name="segmented_image.jpg",
                            mime="image/jpeg"
                        )
                    
                    # Display processing details
                    with st.expander("Processing Details"):
                        st.json({
                            "original_size": image.size,
                            "processed_size": segmented_image.size,
                            "output_path": output_path,
                            "device": DEVICE
                        })

        except Exception as e:
            st.error(f"An error occurred while processing the image: {str(e)}")
            log.error(f"Processing error: {str(e)}")

    # About section
    with st.expander("ℹ️ About"):
        st.markdown("""
        This application uses a U2NET model to segment clothing items in images.
        The segmentation process identifies different parts of the clothing and creates
        separate masks for each component.
        
        **Supported formats:**
        - JPG/JPEG
        - PNG
        
        **Model capabilities:**
        - Identifies up to 4 different clothing components
        - Processes images up to 768x768 pixels
        - Creates alpha masks for each component
        
        **Processing device:** {DEVICE}
        """)

    # Footer
    st.markdown("""
        ---
        Made with ❤️ using Streamlit and U2NET
    """)

if __name__ == "__main__":
    main()
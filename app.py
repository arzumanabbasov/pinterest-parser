import streamlit as st
from utils import PinterestImageExtractor, create_zip
import base64

st.title("Pinterest Image Downloader")

# Input: Text area for entering Pinterest post URLs
urls = st.text_area("Enter Pinterest URL ( using "," as separator )")
post_urls = urls.split(',')

# Button to trigger image download and zip creation
if st.button("Download Images"):
    st.info("Downloading images. Please wait...")

    # Download images and create zip file
    extractor = PinterestImageExtractor(post_urls)
    img_paths = extractor.run()
    zip_filename = 'images.zip'
    create_zip(img_paths, zip_filename)

    # Stream the zip file directly to the user
    with open(zip_filename, 'rb') as file:
        zip_data = file.read()
        zip_b64 = base64.b64encode(zip_data).decode()
        st.success("Download complete!")
        st.markdown(f"### [Download Zip File](data:application/zip;base64,{zip_b64})", unsafe_allow_html=True)

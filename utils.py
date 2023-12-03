import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile


class PinterestImageExtractor:
    def __init__(self, post_urls):
        self.post_urls = post_urls

    def run(self):
        output_dir = "data/"
        os.makedirs(output_dir, exist_ok=True)

        img_paths = []  # To store the paths of downloaded images

        for idx, post_url in enumerate(self.post_urls):
            response = requests.get(post_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                img_url = soup.find("img").get("src")
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    img_extension = img_url.split(".")[-1]
                    img_filename = f"image_{idx + 1}.{img_extension}"
                    img_path = os.path.join(output_dir, img_filename)
                    with open(img_path, "wb") as img_file:
                        img_file.write(img_response.content)
                    img_paths.append(img_path)
                    print(f"Downloaded {img_filename}")
                else:
                    print(f"Failed to download image from post {idx + 1}")
            else:
                print(f"Failed to fetch post {idx + 1}")

        return img_paths


def create_zip(img_paths, zip_filename):
    with ZipFile(zip_filename, 'w') as zip_file:
        for img_path in img_paths:
            zip_file.write(img_path, os.path.basename(img_path))


from selenium import webdriver  # Browser Automation
import requests  # HTTP library for Python API
# for more details about requests :
# https://docs.python-requests.org/en/latest/user/quickstart/
import io
from PIL import Image
import os

# create a new directory to save images
# put a slash at end, or it will save images outside the path
path = "./images/"
try:
    os.makedirs(path)
except FileExistsError:
    # directory already exists
    pass

driver_path = "D:\\Codes\\Selenium\\chromedriver.exe"

wd = webdriver.Chrome(driver_path)

image_link = "https://cdn.pixabay.com/photo/2014/11/30/14/11/cat-551554__340.jpg"


def download_image(download_path, url, file_name):
    try:

        # get the content of image through the url
        # requests.content fetches the body content as bytes from response object
        # requests.get(url) gets the response object from the url
        # we can use requests.text as the content of the body will be encoded automatically
        # better to use .content wisely with custom encoding technique
        image_content = requests.get(url).content

        # store the content as a binary datatype in our device memory
        # this is the best practice to store content of image as Bytes(binary dtypes)
        image_file = io.BytesIO(image_content)

        # convert the binary data into image
        image = Image.open(image_file)

        file_path = download_path + file_name

        # open a file at the file_path using write byte mode
        # and load that file as f
        # save this file as JPEG format
        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Downloaded")

    except Exception as e:
        print("Failed- ", e)


download_image(path, image_link, "test_image.jpg")

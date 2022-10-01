import time
from selenium.webdriver.common.by import By
from selenium import webdriver  # Browser Automation
import requests  # HTTP library for Python API
# for more details about requests :
# https://docs.python-requests.org/en/latest/user/quickstart/
import io
from PIL import Image
import os
import time

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


def get_image_urls(wd, delay, max_images):

	# url of the page that will be scraped
	url = "https://www.google.com/search?q=cat&hl=en&sxsrf=AOaemvLfyTmY-nEy_BNQyll4YEusl7BtDQ:1635600480233&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiav_HMnvLzAhUUIbcAHYYpBK4Q_AUoAXoECAIQAw&biw=1046&bih=972&dpr=1"

	# use webdriver to get the html source of this url page
	wd.get(url)  # this will load this page with webdriver

	# create a empty set for images urls of the page
	# dont want to have duplicate urls,
	# so, using set instead of list
	image_urls = set()

	# counting the skipping number of
	skip = 0

	# loop till the set has maximum number of image urls
	while len(image_urls) < max_images:
		# now scroll to the end of the page
		scroll_down(wd, 2)

		count = 0

		# get all the thumbnails of the page
		# this will have all the elements of the page,
		# that have class name "Q4LuWd"
		# the Class_Name is the all images class name inside html properties
		# By is used for filtered groupby function
		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		# now need to loop through all the thumbnails
		for img in thumbnails[len(image_urls) + skip: max_images]:
			# only lool through the thumbnails after those have done
			try:
				img.click() # this will automatically clicks on the thumbnails
				time.sleep(delay)
			except:
				continue  # if any error happens, ignore that and go to next loop

			# get the images of class "n3VNCb" that contains the main image
			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")

			# now loop through the images

			for image in images:

				#check if 1 source is already exist
				# then break and go to next loop
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skip +=1
					break

				# check if contains source tag 'scr'
				# check if source tag contains 'http'
				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					count +=1
					print(f"Found {count} Image Source.")

	return image_urls


# scroll down  function to scroll down to the bottom of the screen
def scroll_down(wd, delay):
	# execute the javascript script for scroll down to the bottom
	wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(delay)

count = 0
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


	except Exception as e:
		print("Failed- ", e)


urls = get_image_urls(wd, 2, 5)
print(urls)

for i, url in enumerate(urls):
	download_image(path,url, str(i)+".jpg")
	count += 1
	print(f"Downloaded {count} Images")

# close the chrome window when done
wd.quit()

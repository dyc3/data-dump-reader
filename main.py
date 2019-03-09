#!/usr/bin/env python3
import PIL.ExifTags
from flask import Flask
from pathlib import Path
import requests
from bs4 import BeautifulSoup

INPUT_FOLDER = Path("./sample/") # TODO: let the user specify folder

app = Flask(__name__)

users = []
messages = []

def get_exif(string): #string is image root
    img = PIL.Image.open(string)
    exif_data = img._getexif()
    return exif_data

class User(object):
	def __init__():
		self.id = None
		self.full_name = None

class Message(object):
	def __init__():
		self.from_user_id = None
		self.to_user_id = None
		self.text = ""

	def get_from_user() -> User:
		pass

def get_all_user_ids(source_path: Path):
	user_ids = []

	with source_path.joinpath("./friends.html").open("r") as f:
		full_text = f.read()
		soup = BeautifulSoup(full_text)
		for element in soup.find_all("div", class_="user"):
			user_ids += [element.find("div", class_="id").getText().strip()]

	return user_ids

def get_full_name_facebook(user_id):
	resp = requests.get("https://www.facebook.com/" + str(user_id))
	resp.raise_for_status()

	soup = BeautifulSoup(resp.text)
	full_name = soup.find(id="fb-timeline-cover-name").find("a").getText()
	return full_name

def read_data_dump(path: Path):
	user_ids = get_all_user_ids(path)
	print(user_ids)

@app.route("/")
def index():
	return "Hello world"

if __name__ == "__main__":
	read_data_dump(INPUT_FOLDER)

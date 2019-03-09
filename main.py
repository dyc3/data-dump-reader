#!/usr/bin/env python3
import PIL.ExifTags
from flask import Flask
from pathlib import Path
import requests
from bs4 import BeautifulSoup

INPUT_FOLDER = Path("./sample/") # TODO: let the user specify folder

users = []
messages = []

def get_exif(string): #string is image root
	img = PIL.Image.open(string)
	exif_data = img._getexif()
	return exif_data

class User(object):
	def __init__(self):
		self.id = None
		self.full_name = None

class Message(object):
	def __init__(self):
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
	if resp.status_code != 200:
		print("failed to get full name for {}, got response {}".format(user_id, resp.status_code))
		return None

	try:
		soup = BeautifulSoup(resp.text)
		full_name = soup.find(id="fb-timeline-cover-name").find("a").getText()
		return full_name
	except:
		print("failed to parse full name for", user_id)
		return None

def read_data_dump(path: Path):
	global users

	user_ids = get_all_user_ids(path)
	print(user_ids)

	for i in user_ids:
		u = User()
		u.id = i
		u.full_name = get_full_name_facebook(i)
		users += [u]

		print(u.id, u.full_name)

def render_user_list():
	rendered = ""

	for user in users:
		item = "<li>"
		item += user.full_name if user.full_name else user.id
		item += "</li>"
		rendered += item

	return rendered

def render_photo_list():
	rendered = ""
	for i in (INPUT_FOLDER / "photos").iterdir():
		item = '<img src="/photos/{}" />'.format(i.name)
		rendered += item
	return rendered

def create_app():
	app = Flask(__name__)
	def run_on_start(*args, **argv):
		read_data_dump(INPUT_FOLDER)
	run_on_start()
	return app
app = create_app()

@app.route("/")
def index():
	with open("./templates/index.html") as f:
		full_text = f.read().replace("$USER_LIST", render_user_list()) \
							.replace("$PHOTO_LIST", render_photo_list())
		return full_text

@app.route("/photos/<filename>")
def get_photo(filename):
	with (INPUT_FOLDER / "photos" / filename).open("rb") as f:
		return f.read()

if __name__ == "__main__":
	app.run()

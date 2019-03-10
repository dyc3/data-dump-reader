#!/usr/bin/env python3
import PIL.ExifTags
import PIL.Image
from flask import Flask
from pathlib import Path
import requests, json
from bs4 import BeautifulSoup
import watson

INPUT_FOLDER = Path("./sample/") # TODO: let the user specify folder

users = []
messages = []

def get_exif(string): #string is image root
	img = PIL.Image.open(string)
	# exif_data = img._getexif().items()
	exif = {
		PIL.ExifTags.TAGS[k]: v
		for k, v in img._getexif().items()
		if k in PIL.ExifTags.TAGS
	}
	return exif

class User(object):
	def __init__(self):
		self.id = None
		self.full_name = None

class Message(object):
	def __init__(self):
		self.from_user_id = None
		self.to_user_id = None
		self.text = ""

	def get_from_user(self) -> User:
		return get_user_by_id(self.from_user_id)

	def get_to_user(self) -> User:
		return get_user_by_id(self.to_user_id)

def get_user_by_id(user_id):
	if user_id == target_user.id:
		return target_user

	for u in users:
		if u.id == user_id:
			return u
	return None

def get_coversation_with(user):
	convo = []
	for m in messages:
		if m.from_user_id == user.id or m.to_user_id == user.id:
			convo += [m]
	return convo


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

def get_all_messages(source_path: Path):
	messages = []

	with source_path.joinpath("./msg.html").open("r") as f:
		full_text = f.read()
		soup = BeautifulSoup(full_text)
		for element in soup.find_all("div", class_="message"):
			m = Message()
			m.from_user_id = element.find("span", class_="from").getText().strip()
			m.to_user_id = element.find("span", class_="to").getText().strip()
			m.text = element.find("span", class_="text").getText().strip()
			messages += [m]

	return messages

def read_data_dump(path: Path):
	global users, target_user, messages

	user_ids = get_all_user_ids(path)
	print(user_ids)

	for i in user_ids:
		u = User()
		u.id = i
		u.full_name = get_full_name_facebook(i)
		users += [u]

		print(u.id, u.full_name)

	target_user = users[0]
	if not target_user.full_name: # FIXME: this is just for presenting
		target_user.full_name = "Jane Doe"
	users = users[1:]

	messages = get_all_messages(path)


def render_user_list():
	rendered = ""

	first = True # FIXME: this is terrible, im sorry
	for user in users:
		item = '<a class="nav-link" id="msgs_{0}_tab" data-toggle="pill" href="#msgs_{0}" role="tab" aria-controls="v-pills-home" aria-selected="true">{1}</a>'.format(user.id, user.full_name if user.full_name else user.id, "active" if first else "")
		first = False
		rendered += item

	return rendered

def render_conversations():
	rendered = ""
	for i in range(len(users)):
		user = users[i]
		convo = get_coversation_with(user)

		item = '<div class="tab-pane fade" id="msgs_{0}" role="tabpanel" aria-labelledby="msgs_{0}">'.format(user.id, "show active" if i == 0 else "")
		for msg in convo:
			item += '<div>'
			from_user = msg.get_from_user()
			# if from_user ==
			item += '<strong>{}</strong>: {}'.format(from_user.full_name if from_user.full_name else from_user.id, msg.text)
			item += '</div>'
		item += '</div>'

		rendered += item
	return rendered

def render_photo_list():
	rendered = ""
	for i in (INPUT_FOLDER / "photos").iterdir():
		exif = get_exif(i) if i.suffix.lower() in [".jpg", ".jpeg", ".jpe"] else ""

		item = '<div class="card col-3">'
		item += '<img class="img-thumbnail" src="/photos/{}" />'.format(i.name)
		item += '<div>'
		for key, value in exif:
			item += '{} = {}<br />'.format(key, value)
		item += '</div>'
		item += '</div>'
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
							.replace("$TARGET_USER", target_user.full_name) \
							.replace("$PHOTO_LIST", render_photo_list()) \
							.replace("$USER_CONVERSATIONS", render_conversations())
		return full_text

@app.route("/photos/<filename>")
def get_photo(filename):
	with (INPUT_FOLDER / "photos" / filename).open("rb") as f:
		return f.read()

@app.route("/messages/<user_id>")
def get_messages(user_id):
	return json.dumps(get_coversation_with(get_user_by_id(user_id)))

if __name__ == "__main__":
	app.run()

#!/usr/bin/env python3
import PIL.ExifTags
from flask import Flask
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

@app.route("/")
def index():
	return "Hello world"

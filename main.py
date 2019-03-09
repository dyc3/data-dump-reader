#!/usr/bin/env python3
from flask import Flask
app = Flask(__name__)

users = []
messages = []

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
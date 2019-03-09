#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

URL_FACEBOOK_TEMPLATE = "https://www.facebook.com/"
EXAMPLE_PROFILE="https://www.facebook.com/stephanie.kerns.735"

def get_full_name_facebook(user_id):
	resp = requests.get(URL_FACEBOOK_TEMPLATE + str(user_id))
	resp.raise_for_status()

	soup = BeautifulSoup(resp.text)
	full_name = soup.find(id="fb-timeline-cover-name").find("a").getText()
	return full_name

print("stephanie.kerns.735 ->", get_full_name_facebook("stephanie.kerns.735"))

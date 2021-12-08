import time
import vk
from typing import List

class User:
	def __init__(self, id, first_name, last_name, bdate):
		self.id = id
		self.first_name = first_name
		self.last_name = last_name
		self.bdate = bdate


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_bdates(api: vk.API, members: List[int], delay: float = 0.4):
	birth_dates = []
	for chunk in chunks(members, 1000):
		user_ids = ",".join([str(e) for e in chunk])
		response = api.users.get(user_ids=user_ids, fields="bdate")

		for user in response:
			if "bdate" in user:
				birth_dates.append(User(user["id"], user["first_name"], user["last_name"], user["bdate"]))
		time.sleep(delay)

	return birth_dates

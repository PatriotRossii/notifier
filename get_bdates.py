import time
import vk
from typing import Set


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_bdates(api: vk.API, members: Set[int], delay: float = 0.4):
	birth_dates = []
	for chunk in chunks(members, 1000):
		user_ids = ",".join([str(e) for e in chunk])
		response = api.users.get(user_ids=user_ids, fields="bdate")

		for user in response:
			if "bdate" in user:
				birth_dates.append(user["bdate"])

	return birth_dates

import configparser
import datetime
import schedule
import random
import vk
import time

from get_bdates import get_bdates, User
from get_members import get_members

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


DEFAULT_CONFIG_FILENAME = "config.ini"
GROUPS_IDS = [
	129035828, 25583882, 208506918, 169093432, 183594815,
	159392816, 28420497, 192142766, 204467153, 56551328,
	20346, 174259579, 183923310, 137238754, 139018405,
	112408320, 165675212, 175697200, 44872321, 141977955,
	181631203
]

def get_config(filename):
	config = configparser.ConfigParser()
	config.read(filename)
	return config


def get_user_access_token(config) -> str:
	return config["DEFAULT"]["USER_ACCESS_TOKEN"]


def get_group_access_token(config) -> str:
	return config["DEFAULT"]["GROUP_ACCESS_TOKEN"]


def get_list_owner_id(config) -> str:
	return config["DEFAULT"]["GROUP_LIST_DIALOG_OWNER_ID"]


def main():
	config = get_config(DEFAULT_CONFIG_FILENAME)
	
	current_date = datetime.datetime.now().strftime("%-d.%-m")

	group_session = vk.Session(access_token=get_group_access_token(config))
	group_api = vk.API(group_session, v="5.131")

	user_session = vk.Session(access_token=get_user_access_token(config))
	user_api = vk.API(user_session, v="5.131")

	anniversaries = []
	owner_id = int(get_list_owner_id(config))
	members = {}

	for group_id in GROUPS_IDS:
		try:
			for user in get_members(user_api, group_id, "bdate,last_seen,sex"):
				members[user["id"]] = user
		except:
			pass
	last_month = time.time() - (31 * 24 * 3600)
	members = filter(lambda x: x['sex'] == 2 and ('last_seen' in x and x["last_seen"]["time"] > last_month) and 'bdate' in x, members.values())
	for user in members:
		user_bdate = ".".join(user["bdate"].split(".")[:2])
		if user_bdate == current_date:
			anniversaries.append(user)

	for chunk in chunks(anniversaries, 75):
		output_message = ", ".join(
			[f"[id{user['id']}|{user['first_name']} {user['last_name']}]" for user in chunk]
		)
		if output_message:
			group_api.messages.send(message=output_message, peer_id=owner_id, random_id=random.randint(0, 2**32))

if __name__ == "__main__":
	main()

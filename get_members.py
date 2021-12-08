import time
import vk

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_members(api: vk.API, group_id: int, fields: str = "", delay: float = 0.4):
	spy_requests = api.groups.getMembers(group_id=group_id, fields=fields)
	count = spy_requests["count"]
	members = set([item["id"] for item in spy_requests["items"]])

	if count > 1000:
		for i in range(1, (count // 1000) + 1):
			time.sleep(delay)
			members.update(
				set([item["id"] for item in api.groups.getMembers(group_id=group_id, fields=fields, offset=i*1000)["items"]])
			)
	return list(members)

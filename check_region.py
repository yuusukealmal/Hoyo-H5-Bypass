import requests


async def check_region(servers, token):
    BASE = "https://api-account-os.hoyoverse.com/binding/api/getUserGameRolesByLtoken?game_biz=hk4e_global&region={}"

    region_list = []

    for server in servers:
        url = BASE.format(server)
        r = requests.get(url, cookies=token).json()
        if r["retcode"] == 0:
            region_list.append(
                {
                    "nickname": r["data"]["list"][0]["nickname"],
                    "region": r["data"]["list"][0]["region"],
                    "uid": r["data"]["list"][0]["game_uid"],
                }
            )

    return region_list

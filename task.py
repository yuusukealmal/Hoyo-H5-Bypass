import requests


async def get_tasks_id(event_id, token):
    URL = "https://sg-hk4e-api.hoyoverse.com/event/merlin_v2/v3/flow/run/hk4e_global/{}/1?game_biz=hk4e_global"

    r = requests.get(URL.format(event_id), cookies=token).json()
    return r


async def finish_task(tasks, region, token):
    for task in tasks["tasks"]:
        try:
            URL = "https://sg-hk4e-api.hoyoverse.com/event/merlin_v2/v3/flow/run/hk4e_global/{}/2?game_biz=hk4e_global"
            r = requests.get(
                URL.format(tasks["eventid"]), cookies=token, params={"task_id": task}
            ).json()
            print(r)
            if r["retcode"] in [0, 2007, 2004]:
                print(
                    "{} {} {} Task{} 已完成".format(
                        region["region"], region["nickname"], tasks["name"], task
                    )
                )
            else:
                print(
                    "{} {} Task{} 可能有發生錯誤或是有強制性任務 {}".format(
                        region["region"], region["nickname"], task, r["message"]
                    )
                )
        except Exception as e:
            print(
                "{} {} Task{} 發生錯誤 {} {}".format(
                    region["region"], region["nickname"], task, r["message"], e
                )
            )

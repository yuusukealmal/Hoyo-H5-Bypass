import asyncio
import json
import inquirer
from base_token import get_base_token, get_hk4e_token
from check_region import check_region
from task import get_tasks_id, finish_task

server_map = {"1": "os_asia", "2": "os_cht", "3": "os_usa", "4": "os_euro"}

def ask(message, choices):
    questions = [
        inquirer.List("ans", message=message, choices=choices, default=None),
    ]
    return inquirer.prompt(questions)["ans"]


async def main(get_task):
    account = input("請輸入帳號: ")
    password = input("請輸入密碼: ")
    server_input = input("請輸入欲完成的伺服器 (用空格隔開):\n1. 亞服\n2. 台港澳\n3. 美服\n4. 歐服\n").split()

    server_list = [server_map[num] for num in server_input if num in server_map]

    if account.strip() == "" or password.strip() == "":
        print("請輸入帳號或密碼")
        return main(get_task)

    token = await get_base_token(account, password)
    region_list = await check_region(server_list, token)

    for region in region_list:
        e_hk4e_token = await get_hk4e_token(region, token)
        if e_hk4e_token is None:
            raise Exception("Failed to get e_hk4e_token")
        region["e_hk4e_token"] = e_hk4e_token

    with open("event.json", "r", encoding="utf-8") as f:
        task_json = json.load(f)
    selected = ask("請選擇活動", [event["name"] for event in task_json[:5]])
    selected_event = next(
        (event for event in task_json[:5] if event["name"] == selected), None
    )
    if get_task:
        token["e_hk4e_token"] = region_list[0]["e_hk4e_token"]
        tasks = await get_tasks_id(token)
        with open("event.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            data[0]["tasks"] = [task["task_id"] for task in tasks["data"]["tasks"]]
        with open("event.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    else:
        for region in region_list:
            token["e_hk4e_token"] = region["e_hk4e_token"]
    await finish_task(selected_event, region, token)


if __name__ == "__main__":
    try:
        asyncio.run(main(False))
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")

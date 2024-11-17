import requests
from decouple import config


webhook_url = f"{config('BASE_URL')}/{config('TG_BOT_SECRET_KEY')}/notify-door"
domofon_id = 20
tenant_id = 22069


def emulate_doorbell_press_get():
    try:
        print(f"Эмуляция звонка GET")
        url = f"{webhook_url}?domofon_id={domofon_id}&tenant_id={tenant_id}"
        response = requests.get(url)
        if response.status_code == 200:
            print("Успешная эмуляция GET")
            print(f"Response: {response.text}")
        else:
            print(f"Failed to simulate doorbell press via GET. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"An error occurred while simulating GET request: {str(e)}")


def emulate_doorbell_press_post():
    try:
        print(f"Эмуляция звонка POST")
        data = {
            'domofon_id': domofon_id,
            'tenant_id': tenant_id,
        }
        response = requests.post(webhook_url, json=data)
        if response.status_code == 200:
            print("Успешная эмуляция POST")
            print(f"Response: {response.text}")
        else:
            print(f"Failed to simulate doorbell press via POST. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"An error occurred while simulating POST request: {str(e)}")


if __name__ == "__main__":
    emulate_doorbell_press_get()
    # emulate_doorbell_press_post()
    # method = input("Выберите метод для симуляции (GET/POST): ").strip().upper()
    #
    # if method == 'GET':
    #     pass
    # elif method == 'POST':
    # else:
    exit()

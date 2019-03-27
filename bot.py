import json
import requests
import time
import urllib


TOKEN = "687340460:AAE0ThDoRNnMiXr5dZAxSY68C4R4AzNUJpg"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
IMAGE_API_URL = "https://pixabay.com/api/?key=12005214-6f8260241d904f7e38503e6b0&q="


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_image_url(text):
    try:
        contents = requests.get(IMAGE_API_URL + text).json()
        if len(contents["hits"]) > 0:
            image = contents["hits"][0]
            url = image['largeImageURL']
        else:
            url = "Картинок на такой запрос нет :("
    except ConnectionError:
        url = "Картиночки не загрузились :("
    return url


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        if "text" in update["message"]:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            img_url = get_image_url(text)
            try:
                send_message(text, chat)
                if img_url == "Картинок на такой запрос нет :(" or img_url == "Картиночки не загрузились :(":
                    send_message(img_url, chat)
                else:
                    send_image(img_url, chat)
            except ConnectionError:
                print("Сообщеньки не отправились :(")


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text, chat_id


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def send_image(image, chat_id):
    image = urllib.parse.quote_plus(image)
    url = URL + "sendPhoto?photo={}&chat_id={}".format(image, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        try:
            updates = get_updates(last_update_id)
        except ConnectionError:
            print("Никак не достучаться до телеграмма :(")
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()

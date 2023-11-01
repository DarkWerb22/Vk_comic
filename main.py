import os
import requests
import random

from dotenv import load_dotenv


def download_comic(url, path):
    response = requests.get(url)
    response.raise_for_status()
    comic = response.json()
    picture_path = comic["img"]
    comic_comment = comic["alt"]
    picture_response = requests.get(picture_path)
    picture_response.raise_for_status()
    with open(path, "wb") as file:
        file.write(picture_response.content)
    return comic_comment


def check_vk_response(response):
    vk_response = response.json()
    if "error" in vk_response:
        raise Exception("Exception api")
    else:
        return vk_response


def get_upload_server(token, group_id):
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    params = {
        "access_token": token,
        "v": "5.130",
        "group_id": group_id
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    vk_response = check_vk_response(response)
    return vk_response['response']


def upload_image(url, path):
    with open(path, "rb") as file:
        files = {
            "photo": file
        }
        response = requests.post(url, files=files)
    response.raise_for_status()
    image_response = response.json()
    return image_response


def save_photo(token, group_id, photo, hash_image, server):
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    params = {
        "v": "5.154",
        "access_token": token,
    }
    data = {
        "photo": photo,
        "hash": hash_image,
        "server": server,
        "group_id": group_id
    }
    response = requests.post(url, params=params, data=data)
    response.raise_for_status()
    vk_response = check_vk_response(response)
    return vk_response["response"]


def post_photo(token, group_id, attachments, message):
    url = "https://api.vk.com/method/wall.post"
    params = {
        "owner_id": f"-{group_id}",
        "v": "5.154",
        "access_token" : token,
        "attachments": attachments,
        "message": message
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    vk_response = check_vk_response(response)
    return vk_response["response"]


if __name__=="__main__":
    load_dotenv()
    token = os.environ["VK_TOKEN"]
    group_id = os.environ["VK_GROUP_ID"]
    comics_amount = 2842
    comic_number = random.randint(1, comics_amount)
    try:
        upload_server = get_upload_server(token, group_id)
        upload_url = upload_server["upload_url"]

        comic_url = f"https://xkcd.com/{comic_number}/info.0.json"
        comic_comment = download_comic(comic_url, path=f"comic_{comic_number}.png")

        upload_response = upload_image(upload_url, f"comic_{comic_number}.png")
        server = upload_response["server"]
        hash_image = upload_response["hash"]
        photo = upload_response["photo"]

        save_response = save_photo(token, group_id, photo, hash_image, server)
        attachments=f"photo{save_response[0]['owner_id']}_{save_response[0]['id']}"
        post_photo(token, group_id, attachments, message=comic_comment)
    except Exception as e:
        print("Произошла ошибка", e)
    finally:
        os.remove(path=f"comic_{comic_number}.png")
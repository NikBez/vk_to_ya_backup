import sys
import json
from environs import Env
import requests

from assets import get_image_filename, get_biggest_img


def main():
    try:
        user_id = int(input('Enter VK user ID: '))
    except ValueError:
        print('Invalid ID')
        return

    vk_request = VK_Handler(vk_access_token, user_id)
    vk_response = vk_request.get_profile_photos()

    data_to_upload = []
    user_meta = []
    likes = []
    for photo in vk_response['response']['items']:
        filename = get_image_filename(photo, likes)
        likes.append(photo['likes']['count'])
        url, size = get_biggest_img(photo)
        data_to_upload.append({
            'filename': filename, 
            'url': url,   
        })
        user_meta.append({
            'filename': filename,
            'size': size
        })
    with open(f'./meta/id_{user_id}.json', 'w') as file:
        json.dump(user_meta, file, ensure_ascii=False, indent=2)

    ya_user_folder_path = f'From Netology/id_{user_id}'
    uploader = YaUploader(ya_access_token)
    print(f'Creating folder in Yandex Disk...')
    uploader.create_folder(ya_user_folder_path)
    print('Uploading photos to Yandex disk...')
    for image in data_to_upload:
        file_path = f'{ya_user_folder_path}/{image["filename"]}'
        uploader.upload(file_path, image['url'], image['filename'])
    print('Task is complite!')


class VK_Handler:
   def __init__(self, vk_access_token, user_id, version='5.131'):
       self.params = {
           'user_id': user_id,
           'feed_type': 'photo',
           'access_token': vk_access_token,
           'v': version
       }

   def get_profile_photos(self, album_id='profile', extended=1):
       url = 'https://api.vk.com/method/photos.get'
       params = {
           'album_id': album_id,
           'extended': extended,
       }
       response = requests.get(url, params={**self.params, **params})
       response = response.json()
       if not response.get('error'):
           print('Get data from VK')
           return response
       print(f'Error code: {response["error"]["error_code"]}. {response["error"]["error_msg"]}')
       sys.exit()


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str, image_url: str, filename):
        """Метод загружает файл на яндекс диск"""

        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'url': image_url, 'path': file_path}
        headers = {
            'Authorization': f'OAuth {self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, params=params, headers=headers)
        if 200 <= response.status_code < 300:
            print(f'Success, image {filename} is saved')
        else:
            print(f'Error: {response.status_code}')

    def create_folder(self, path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {
            'Authorization': f'OAuth {self.token}',
        }
        response = requests.put(url, params={'path': path}, headers=headers)
        response = response.json()
        if response.get('message'):
            print(response['message'], response['description'])
        else:
            print(f'Folder {path} was created.')


if __name__ == '__main__':
    env = Env()
    env.read_env()
    vk_access_token = env('VK_ACCESS_TOKEN')
    ya_access_token = env('YANDEX_POLIGON_TOKEN')
    main()






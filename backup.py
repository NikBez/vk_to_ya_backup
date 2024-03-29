import argparse
import sys

import requests
from environs import Env

from assets import parse_image_response, save_images_meta

MAX_COUNT = 5


def main(args):
    if not args.id:
        try:
            user_id = int(input('Enter VK user ID: '))
        except ValueError:
            print('Invalid ID')
            return
    else:
        user_id = args.id

    vk_request = VK_Handler(vk_access_token, user_id)
    vk_response = vk_request.get_profile_photos(args)

    data_to_upload, user_meta = parse_image_response(vk_response, MAX_COUNT)
    save_images_meta(user_meta, user_id)

    uploader = YaUploader(ya_access_token)

    print('Creating folder in Yandex Disk...')
    ya_user_folder_path = f'{ya_folder_path}/id_{user_id}'
    uploader.create_folder(ya_user_folder_path)

    print('Uploading photos to Yandex disk...')
    for image in data_to_upload:
        file_path = f'{ya_user_folder_path}/{image["filename"]}'
        uploader.upload(file_path, image['url'], image['filename'])
    print('Task is complite!')


class VK_Handler:
    """Connect to VK API by special user id"""

    def __init__(self, vk_access_token, user_id, version='5.131'):
        self.params = {
            'user_id': user_id,
            'feed_type': 'photo',
            'access_token': vk_access_token,
            'v': version,
        }

    def get_profile_photos(self, args, extended=1):
        """Method gets profile photos of special user"""

        url = 'https://api.vk.com/method/photos.get'
        params = {
            'album_id': args.album,
            'extended': extended,
            'rev': args.rev,
        }
        response = requests.get(url, params={**self.params, **params})
        response = response.json()
        if not response.get('error'):
            print('Get data from VK')
            return response
        print(f'Error code: '
              f'{response["error"]["error_code"]}. '
              f'{response["error"]["error_msg"]}'
              )
        sys.exit()


class YaUploader:
    """Connect to YA API"""

    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str, image_url: str, filename):
        """Method uploads photos to yandex disk"""

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
        """Method takes path and crates folder in yandex disk on it"""

        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {
            'Authorization': f'OAuth {self.token}',
        }
        response = requests.put(url, params={'path': path}, headers=headers)
        json_response = response.json()
        if json_response.get('message'):
            print(json_response['message'], json_response['description'])
        else:
            print(f'Folder {path} was created.')
        return response


if __name__ == '__main__':
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id', help='VK id of user', type=int)
    parser.add_argument('-a',
                        '--album',
                        default='profile',
                        choices=['profile', 'wall', 'saved'],
                        help='Albums to upload',
                        type=str
                        )
    parser.add_argument('-r', '--rev', default=0, help='Sorting order', type=int)
    args = parser.parse_args()

    vk_access_token = env('VK_ACCESS_TOKEN')
    ya_access_token = env('YANDEX_POLIGON_TOKEN')
    ya_folder_path = env('YANDEX_DISK_FOLDER_PATH')
    main(args)

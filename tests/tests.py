import requests
from environs import Env

from backup import YaUploader

env = Env()
env.read_env()
ya_access_token = env('YANDEX_POLIGON_TOKEN')
ya_folder_path = env('YANDEX_DISK_FOLDER_PATH')
test_folder = '/test_folder'


class TestCreateFolder:

    def test_successful_create_folder(self):
        delete_test_folder()
        test = YaUploader(ya_access_token)
        response = test.create_folder(ya_folder_path + test_folder)
        assert response.status_code == 201

    def test_folder_exist(self):
        test = YaUploader(ya_access_token)
        response = test.create_folder(ya_folder_path + test_folder)
        assert response.status_code == 409


def delete_test_folder():
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {
        'Authorization': f'OAuth {ya_access_token}',
    }
    requests.delete(url, params={'path': ya_folder_path + test_folder}, headers=headers)

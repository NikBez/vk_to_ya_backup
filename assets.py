import json


def get_image_filename(image, likes):
    if image['likes']['count'] in likes:
        return f'{image["likes"]["count"]}_{image["date"]}.jpg'
    return f'{image["likes"]["count"]}.jpg'


def get_biggest_img(photo):
    """Function parse JSON data and choose a biggest available option to save"""

    sizes = 'wzyxmsrqpo'
    max_index = float('inf')
    photo_url = ''
    for size in photo['sizes']:
        current_index = sizes.index(size['type'])
        if current_index < max_index:
            max_index = current_index
            photo_url = size['url']
    return photo_url, sizes[max_index]


def parse_image_response(vk_response, max_count):
    """Function takes response from VK and maximum count of images need to save.
    Returns two lists:
        - 'user_meta' for save to json
        - 'data_to_upload' for work with Ya API
    """

    data_to_upload = []
    user_meta = []
    likes = []
    count = 0
    for photo in vk_response['response']['items']:
        if count == max_count:
            break
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
        count += 1
    return data_to_upload, user_meta


def save_images_meta(meta, user_id):
    with open(f'./meta/id_{user_id}.json', 'w') as file:
        json.dump(meta, file, ensure_ascii=False, indent=2)

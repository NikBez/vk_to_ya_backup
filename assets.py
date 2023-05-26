def get_image_filename(image, likes):
    if image['likes']['count'] in likes:
        return f'{image["likes"]["count"]}_{image["date"]}.jpg'
    return f'{image["likes"]["count"]}.jpg'


def get_biggest_img(photo):
    sizes = 'wzyxmsrqpo'
    max_index = float('inf')
    photo_url = ''
    for size in photo['sizes']:
        current_index = sizes.index(size['type'])
        if current_index < max_index:
            max_index = current_index
            photo_url = size['url']
    return photo_url, sizes[max_index]





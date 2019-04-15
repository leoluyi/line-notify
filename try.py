'''
測試 Line Notify
'''
from dotenv import load_dotenv
from io import BytesIO
import matplotlib as mpl
import os
from pathlib import Path
import requests
import validators
from datetime import datetime
mpl.use('TkAgg')
load_dotenv()

LINE_NOTIFY_API_TOKEN = os.environ['LINE_NOTIFY_API_TOKEN']


def line_notify(token, msg, image=None, sticker=None):
    '''[summary]

    [description]

    Arguments:
        token {str} -- [description]
        msg {str} -- [description]

    Keyword Arguments:
        sticker {tuple} -- tuple(stickerPackageId, stickerId) (default: {None})

    Returns:
        [type] -- [description]
    '''

    url = f'https://notify-api.line.me/api/notify'
    headers = {
        "Authorization": "Bearer " + token,
    }

    payload = {
        'message': msg,
    }

    if sticker:
        payload['stickerPackageId'] = sticker[0]
        payload['stickerId'] = sticker[1]

    files = None
    if image:
        if validators.url(image):
            print(f'Use image url: {image}')
            response = requests.get(image)
            img_bin = BytesIO(response.content)
        else:
            print(f'Use local image: "{Path(image).expanduser().resolve()}"')
            img_bin = open(Path(image).expanduser().resolve(), 'rb')

        files = {'imageFile': img_bin}

    res = requests.post(url, headers=headers, params=payload, files=files)
    return res.text


def main():
    msg = f'Send from my Python. {datetime.now().isoformat()}'
    # res = line_notify(LINE_NOTIFY_API_TOKEN, msg, sticker=(1, 100))
    res = line_notify(LINE_NOTIFY_API_TOKEN,
                      msg,
                      image='https://scontent.ftpe7-3.fna.fbcdn.net/v/t1.0-9/22310259_10156660655830830_5163678998153783084_n.jpg?_nc_cat=102&_nc_ht=scontent.ftpe7-3.fna&oh=49af1e595ed560c42f547391bca01b97&oe=5D2FD510')
    # res = line_notify(LINE_NOTIFY_API_TOKEN,
    #                   msg,
    #                   image='~/Downloads/test.jpg')
    print(res)


if __name__ == '__main__':
    main()

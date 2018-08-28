import requests
from db import helper
from config import config

def read_comments(url):

    try:
        print('URL: {}'.format(url))
        content = requests.get(url,verify=False).json()
    except Exception:
        return {'data': [], 'next': ''}

    if 'comments' in content:
        comments = content['comments']['data']

        try: next_url = content['comments']['paging']['next']
        except Exception: next_url = ''

    elif 'data' in content:
        comments = content['data']

        try: next_url = content['paging']['next']
        except Exception: next_url = ''

    else:
        return {'data': [], 'next': ''}

    data = []
    for comment in comments:
        collection = helper.init_db(config.db)
        helper.insert_row(collection['fb_comments'], comment, 'id')

    return {'data':data, 'next':next_url}


def scrape_comments(POST_ID, ACCESS_TOKEN):
    URL = 'https://graph.facebook.com/v3.0/' + POST_ID + \
          '?fields=comments.limit(150){id, created_time, message, like_count, comment_count, comments.limit(150){id, created_time, message, like_count, comment_count}}' \
          '&access_token=' + ACCESS_TOKEN

    data = read_comments(URL)
    print(data)

    articles = data['data']
    next_link = data['next']

    while next_link != '':
        data = read_comments(next_link)
        articles = articles + data['data']
        next_link = data['next']


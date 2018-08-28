import requests
from db import helper
from config import config
from web import comment_scraper


def read_posts(url, source, ACCESS_TOKEN):
    try:
        print('URL: {}'.format(url))
        content = requests.get(url,verify=False).json()
    except Exception:
        return {'data': [], 'next': ''}

    if 'posts' in content:
        posts = content['posts']['data']

        try: next_url = content['posts']['paging']['next']
        except Exception: next_url = ''

    elif 'data' in content:
        posts = content['data']

        try: next_url = content['paging']['next']
        except Exception: next_url = ''

    else:
        return {'data': [], 'next': ''}

    data = []
    for post in posts:

        try:
            print('Created time: {}'.format(post['created_time']))
            if post['created_time'][:4] != '2018':
                return {'data': data, 'next': ''}

            print(post)

            article = {'id': post['id'],
                       'timestamp': post['created_time'],
                       'summary': post['message'],
                       'link': post['link'],
                       'type': post['status_type'],
                       'likes' : post['like']['summary']['total_count'],
                       'comments' : post['comments']['summary']['total_count'],
                       'full_picture': post['full_picture'],
                       'thumb_picture': post['picture'],
                       'permalink_url':post['permalink_url'],
                        'love':post['love']['summary']['total_count'],
                        'haha':post['haha']['summary']['total_count'],
                        'wow' :post['wow']['summary']['total_count'],
                        'sad' :post['sad']['summary']['total_count'],
                        'angry':post['angry']['summary']['total_count']
            }
        except Exception as e:
            continue

        try:
            article['shares'] = post['shares']['count']
        except Exception:
            article['shares'] = 0


        try:

            if 'subattachments' in post['attachments']['data']:
                article['attachments'] = post['attachments']['data']['subattachments']
            else:
                article['attachments'] = post['attachments']['data']

            article['description'] = article['attachments'][0]['description']
            article['title'] = article['attachments'][0]['title']

        except Exception as e:
            article['attachments'] = []
            article['description'] = ""
            article['title'] = ""

        # Add news source
        article['source'] = source

        collection = helper.init_db(config.db)

        helper.insert_row(collection['fb_posts'], article, 'id')

        comment_scraper.scrape_comments(article['id'], ACCESS_TOKEN)

    return {'data':data, 'next':next_url}


def scrape_page(FACEBOOK_PAGE_ID, ACCESS_TOKEN):
    URL = 'https://graph.facebook.com/v2.12/' + FACEBOOK_PAGE_ID +\
          '?fields=posts.limit(150)' \
          '{id,created_time,message,attachments,link,permalink_url,shares,%20status_type,%20comments.limit(0).summary(true),reactions.type(LIKE).summary(total_count).as(like),reactions.type(LOVE).summary(total_count).as(love),reactions.type(HAHA).summary(total_count).as(haha),reactions.type(WOW).summary(total_count).as(wow),reactions.type(SAD).summary(total_count).as(sad),reactions.type(ANGRY).summary(total_count).as(angry),full_picture,picture}&access_token=' + ACCESS_TOKEN + '&pretty=0;'


    data = read_posts(URL, FACEBOOK_PAGE_ID,ACCESS_TOKEN)
    print(data)

    articles = data['data']
    next_link = data['next']

    while next_link != '':
        data = read_posts(next_link, FACEBOOK_PAGE_ID)
        articles = articles + data['data']
        next_link = data['next']


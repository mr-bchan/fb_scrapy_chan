# Script to read Facebook Page posts using Facebook Graph API
# Input
# @ FACEBOOK_PAGE_ID
# @ ACCESS TOKEN - valid and not expired


from config import config, fb_pages
from web import post_scraper

if __name__ == '__main__':

    facebook_page_ids = fb_pages.FACEBOOK_PAGE_IDS

    print('Facebook pages for scraping: {} \n'.format(facebook_page_ids))


    for id in facebook_page_ids:
       post_scraper.scrape_page(id, config.ACCESS_TOKEN)


import re
import sys
from urllib import quote, unquote
import xbmcaddon
from resources.lib import scraper, utils

### get addon info
__addon__             = xbmcaddon.Addon()
__addonid__           = __addon__.getAddonInfo('id')
__addonidint__        = int(sys.argv[1])

def main(params):
    if not params.has_key('mode') or params['mode'] == 'list_categories':
        html = scraper.open_page('http://thenewboston.org/tutorials.php')
        categories = scraper.get_categories(html)
        for category in categories:
            utils.add_directory_link(category['title'], 
                                     'http://thenewboston.org/images/theNewBoston_logo.png', 
                                     'list_topics', 
                                     category['title'], 
                                     isFolder=True, 
                                     totalItems=20)

    elif params['mode'] == 'list_topics':
        title = params['url']
        html = scraper.open_page('http://thenewboston.org/tutorials.php')
        topics = scraper.get_topics(html, title)
        for topic in topics:
            utils.add_directory_link(topic['title'], 
                                     'http://thenewboston.org/images/theNewBoston_logo.png', 
                                     'list_lessons', 
                                     quote(topic['url']), 
                                     isFolder=True, 
                                     totalItems=int(topic['count']))

    elif params['mode'] == 'list_lessons':
        url = unquote(params['url'])
        html = scraper.open_page(url)
        lessons = scraper.get_lessons(html)
        for lesson in lessons:
            utils.add_directory_link(lesson['title'], 
                                     'http://thenewboston.org/images/theNewBoston_logo.png', 
                                     'play_video', 
                                     quote(lesson['url']), 
                                     isFolder=False, 
                                     totalItems=1)


    elif params['mode'] == 'play_video':
        html = scraper.open_page(unquote(params['url']))
        youtube_url, youtube_id = scraper.get_youtube(html)
        url = "plugin://plugin.video.youtube?action=play_video&videoid={0}".format(youtube_id)
        play_video(url)

    utils.end_directory()

if __name__ == '__main__':
    params = utils.get_params()
    main(params)

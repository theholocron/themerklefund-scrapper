from base import AbstractURLScraper


class IcoWatchListURLScraper(AbstractURLScraper):

    @property
    def base_url(self):
        return 'https://www.icowatchlist.com/'

    @property
    def available_filters(self):
        return ['live', 'upcoming']

    @property
    def homepage_html_tags(self):
        return ('div', {"class": "logo-div"})

    @property
    def elements_filter(self):
        return ('findChild', 'a', 'get', 'href')

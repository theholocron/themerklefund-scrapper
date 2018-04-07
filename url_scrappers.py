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


class IcoDataURLScraper(AbstractURLScraper):

    @property
    def base_url(self):
        return 'https://www.icodata.io/ICO/'

    @property
    def available_filters(self):
        return ['active', 'upcoming']

    @property
    def homepage_html_tags(self):
        return ('tr', {"class": "item"})


class CryptoSlateURLScraper(AbstractURLScraper):

    @property
    def base_url(self):
        return 'https://cryptoslate.com/ico-database/'

    @property
    def available_filters(self):
        return ['', 'pre-icos', 'upcoming-icos']

    @property
    def homepage_html_tags(self):
        return ('div', {"class": "row"})

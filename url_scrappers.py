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
    def ico_url(self):
        return self.base_url


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

    @property
    def ico_url(self):
        return 'https://www.icodata.io'


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

    @property
    def ico_url(self):
        return ''


class FoundIcoURLScraper(AbstractURLScraper):

    @property
    def base_url(self):
        return 'https://foundico.com/'

    @property
    def available_filters(self):
        return ['#ico-pan-1','#ico-pan-2']

    @property
    def homepage_html_tags(self):
        return ('div',{'class':'ii-b-btn'})

    @property
    def ico_url(self):
        return self.base_url


class CryptocoinchartsURLScraper(AbstractURLScraper):

    @property
    def base_url(self):
        return 'https://cryptocoincharts.info/ico?page=1&cats=0&bc=0&type='

    @property
    def available_filters(self):
        return ['upcoming', 'current','completed']

    @property
    def homepage_html_tags(self):
        return ('td',{'class':'ico_first_line'})

    @property
    def ico_url(self):
        return 'https://cryptocoincharts.info'


class ICObenchURLScraper(AbstractURLScraper):

    @property
    def base_url(self):
          return 'https://icobench.com/icos'

    @property
    def available_filters(self):
        return ['',]

    @property
    def homepage_html_tags(self):
        return ('div',{'class':'content'})

    @property
    def ico_url(self):
        return 'https://icobench.com'
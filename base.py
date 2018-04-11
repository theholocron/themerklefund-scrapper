import os
import abc
import requests
import pandas as pd
from bs4 import BeautifulSoup


class BaseScraper(object):

    def get_soup(self, url):
        """
        returns a soup object for the contents of the `url`
        """
        response = requests.get(url)
        if response.status_code != 200:
            # self.log_to_slack("<msg>")
            return

        content = response.content
        return BeautifulSoup(content, 'lxml')


class AbstractURLScraper(BaseScraper):

    @abc.abstractproperty
    def base_url(self):
        """
        the home url for the website being scraped
        """

    @abc.abstractproperty
    def available_filters(self):
        """
        top level filters available at the home url
        """

    @abc.abstractproperty
    def homepage_html_tags(self):
        """
        a tuple of properties for the .findAll method to search for on the homepage
        """

    @abc.abstractproperty
    def ico_url(self):
        """
        the url to be added to extracted urls
        """

    @property
    def elements_filter(self):
        return ('findChild', 'a', 'get', 'href')

    def parse_urls(self):
        """
        returns a list of relevant urls scraped for the given child class object
        """
        derived_urls = list()

        for f in self.available_filters:
            url = self.base_url + f
            elements = self.get_soup(url).findAll(*self.homepage_html_tags)

            for element in elements:
                derived_url = self.get_from_element(element)
                if not derived_url:
                    continue
                derived_urls.append(self.ico_url + derived_url)
        return set(derived_urls)

    def get_from_element(self, element):
        """
        returns the url for a given base element
        """
        i = 0
        while i < len(self.elements_filter):
            element = getattr(element, self.elements_filter[i])
            i += 1

            if callable(element):
                element = element(self.elements_filter[i])
                i += 1

            if not element:
                return
        return element


class AbstractDataScraper(BaseScraper):

    @abc.abstractproperty
    def _urls(self):
        """
        the URLScraper object which returns active ICO URLs
        """

    @abc.abstractproperty
    def data_tags(self):
        """
        metadata explaining the list of html-tags we want to extract.
        these html-tags contain the required data_fields we want to extract.
        """

    @property
    def urls(self):
        return self._urls().parse_urls()

    @property
    def base_directory(self):
        return '/Users/nirmal/Desktop/merklefund'

    def parse_urls(self):
        """
        returns a list of required fields from each of urls identified
        for scraping from related URLScraper
        """
        payload = list()

        for url in self.urls:
            soup =  self.get_soup(url)

            data_tags = dict()
            for tag_name, tag_query in self.data_tags:
                tag = soup.findAll(*tag_query)
                data_tags[tag_name] = tag

            fields = list()
            for tag_name, tag in data_tags.iteritems():
                extract_method = getattr(self, tag_name)
                fields += extract_method(tag)
            payload.append(dict(fields))
        return payload

    def download(self):
        payload = self.parse_urls()
        df = pd.DataFrame(payload)
        path = os.path.join(self.base_directory, self.__class__.__name__ + '.csv')
        df.to_csv(path, index=False, encoding='utf-8')

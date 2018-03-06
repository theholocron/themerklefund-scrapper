import abc
import requests
from bs4 import BeautifulSoup


class AbstractURLScraper(object):

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
    def elements_filter(self):
        """
        a tuple of operations/params to run on each element
        """

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
                derived_urls.append(derived_url)
        return set(derived_urls)
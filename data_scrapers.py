from base import AbstractDataScraper
from url_scrapers import (
	IcoWatchListURLScraper,
        IcoDataURLScraper,
        FoundIcoURLScraper,
)

class IcoWatchListDataScraper(AbstractDataScraper):

    @property
    def _urls(self):
        return IcoWatchListURLScraper

    @property
    def data_tags(self):
        data_tags = (
            ('main_table', ['div', {'class':'row _dTLine'}]),
            ('website', ['a', {'class':'btn btn-default btn-lg btn-block btnSuccess oblink'}]),
            ('description', ['div', {'style': "padding: 10px; font-size: 16px;"}]),
            ('short_description', ['p', {'class': "project-long-description"}]),
        )
        return data_tags

    def main_table(self, tag):
        main_table_data = list()

        for element in tag:
            key = element.find('div', {'class': 'col-xs-6 col-md-3'})
            value = element.find('div', {'class': 'col-xs-6 col-md-9'})

            if (not key) or (not value):
                continue

            key_val = key.text.replace('\n', '').replace('\t', '').strip()
            value_val = value.text.replace('\n', '').replace('\t', '').strip()
            main_table_data.append([key_val, value_val])
        return main_table_data

    def website(self, tag):
        return [['website', tag[0].get('href')],]

    def description(self, tag):
        return [['description', tag[0].text.replace('\n', '').replace('\t', '').strip()],]

    def short_description(self, tag):
        return [['short-description', tag[0].text.replace('\n', '').replace('\t', '').strip()],]


class IcoDataDataScraper(AbstractDataScraper):

    @property
    def _urls(self):
        return IcoDataURLScraper

    @property
    def data_tags(self):
        data_tags = (
            ('ico_info', ['div', {'class':'info-ico-stats'}]),
            ('alexa', ['p', {'id':'alexa-stats'}]),
            ('coin_name', ['h1', {'class':'coin-name'}]),
            ('website', ['a', {'class':'website'}]),
            ('description', ['div', {'class': 'other-info'}]),
        )
        return data_tags

    def ico_info(self, tag):
        ico_info_data = list()

        for element in tag[0].findAll('span'):
            key = element.find('strong').text
            value = [string for string in element.strings][-1]

            if (not key) or (not value):
                continue

            key_val = key.replace('\n', '').replace('\t', '').strip()
            value_val = value.replace('\n', '').replace('\t', '').strip()
            ico_info_data.append([key_val, value_val])
        return ico_info_data

    def alexa(self, tag):
        if not tag:
            return [['alexa', '']]
        alexa = [string for string in tag[0].strings if string != '\n'][1]
        alexa = alexa.replace('\n', '').replace('\t', '').strip()
        return [['alexa', alexa]]

    def coin_name(self, tag):
        coin_name = [string for string in tag[0].strings][-1]
        coin_name = coin_name.replace('\n', '').replace('\t', '').strip()
        return [['coin_name', coin_name]]

    def description(self, tag):
        try:
            description = tag[0].find('p')
            description = [string for string in description.strings][-1]
            return [['description', description]]
        except Exception:
            return [['description', '']]

    def website(self, tag):
        return [['website', tag[0].get('href')],]


class FoundIcoDataScraper(AbstractDataScraper):

    @property
    def _urls(self):
        return FoundIcoURLScraper

    @property
    def data_tags(self):
        data_tags = (
            ('name', ['section', {'id': 'ico-head-cont'}]),
            ('summary', ['section', {'id': 'ico-sum-cont'}]),
            ('description', ['section', {'id': 'ico-sum-cont'}]),
            ('table', ['table', {'class': 'smry-table'}]),
            #('social', ['table', {'class': 'smry-table'}]),
        )
        return data_tags

    def name(self, tag):
        name = tag[0].find('h1').text
        name, symbol = name.split('(')
        return [['coin_name', name], ['coin_symbol', symbol.replace(')', '')]]

    def summary(self, tag):
        summary_data = list()
        tags = tag[0].findAll('div', {'class': 'fl-mrk-item mdl-shadow--2dp'})

        for t in tags:
            key = t.find('div', {'class': 'flmrk-title'}).text
            value = t.find('div', {'class': 'flmrk-mark'}).text
            summary_data.append([key, value])

        ico_score = tag[0].find('span', {'class': 'flmf-mark'})
        if ico_score:
            summary_data.append(['ico_score', ico_score.text.split('<a')[0]])
        return summary_data

    def description(self, tag):
        if len(tag) < 2:
            return [['description', '']]
        description = tag[1].find('p').text
        return [['description', description]]

    def table(self, tag):
        table_data = list()
        rows = tag[0].findAll('tr')

        for row in rows:
            elements = row.findAll('td')
            if len(elements) != 3:
                continue
            table_data.append([elements[1].text, elements[2].text])
        return table_data

    def social(self, tag):
        table_data = list()

        for i in range(1, len(tag)):
            rows = tag[i].findAll('tr')
            for row in rows:
                elements = row.findAll('td')
                if len(elements) != 3:
                    continue
                table_data.append([elements[1].text, elements[2].text])
        return table_data

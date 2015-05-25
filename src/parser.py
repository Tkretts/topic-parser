# coding: utf-8

import os
from urlparse import urlparse
import urllib2
from lxml import html

from helpers import iri_to_uri


def split_by_length(line, length):
    """ Split string by words with specified max length
    :param unicode line: Line
    :param int length: Max line length
    :rtype: list
    """
    words = line.split()
    new_line = u''
    lines = []
    for word in words:
        if len(new_line) + len(word) + 1 >= length:
            lines.append(new_line)
            lines.append('\n')
            new_line = ''
        # Split word if it more than length
        new_line += u'\n'.join(
            word[0+i:length+i] for i in range(0, len(word), length)) + ' '
    lines.append(new_line)
    return lines


class Topic(object):
    """ Topic object
    """
    page = None

    def __init__(self, url, config=None):
        """ :param basestring url: Topic URL
            :param dict config: Settings dictionary
        """
        self.url = iri_to_uri(url)
        self.config = config or {}

        self.get_html_result()

    @property
    def template(self):
        """ Resource template to get current URL's config
            :rtype: dict
        """
        templates = self.config.get('templates', {})
        template = 'default'

        for item in templates:
            if item in self.url:
                template = item

        if template not in templates.keys():
            raise AttributeError('Template is not configured')

        return templates[template]

    @property
    def topic_class(self):
        """ Topic's DOM class
            :rtype: basestring
        """
        return self.template.get('class', 'content')

    @property
    def text_header(self):
        """ Get topic's header
        :rtype: unicode
        """
        no_header = '<Header was not parsed>'
        if 'header_class' in self.template.keys():
            header_xpath = ".//body//*[contains(@class, '{0}')]".format(
                self.template.get('header_class'))
        else:
            header_xpath = (
                ".//body//*[contains(@class, '{0}')]/.."
                "//*[starts-with(local-name(), 'h')]".format(
                    self.topic_class))
        try:
            header = self.page.xpath(header_xpath)[0].text
        except IndexError:
            header = no_header
        return header or no_header

    @property
    def text_content(self):
        content_xpath = (
            ".//body//*[contains(@class, '{0}')]//*[local-name()='p' or "
            "starts-with(local-name(), 'h')]".format(
                self.topic_class))
        body = self.page.xpath(content_xpath)
        topic_strings = []
        for p in body:
            topic_strings.append(
                self.process_row(p)
            )
        return topic_strings

    @property
    def resource_name(self):
        return getattr(urlparse(self.url), 'netloc', '')

    @property
    def url_path_list(self):
        path = getattr(urlparse(self.url), 'path', '')
        return filter(lambda x: x, path.split('/'))

    @property
    def file_path(self):
        """ Get topic's file path
            :rtype: basestring
        """
        return os.path.join(self.resource_name, *self.url_path_list[:-1])

    @property
    def file_name(self):
        """ Get topic's file name
            :rtype: basestring
        """
        try:
            res = '{0}.txt'.format(self.url_path_list[-1])
        except KeyError:
            raise KeyError('Could not parse file name from URL. Is it correct?')
        return res

    @property
    def printable_lines(self):
        """ Make topic pretty printable
        :rtype: list
        """
        printable_view = []

        # Print header
        printable_view.append(self.text_header)
        printable_view.append('\n\n')

        # Print body
        for line in self.text_content:
            if line:
                printable_view.extend(self.processed_body_line(line))
                printable_view.append('\n\n')

        return printable_view

    def get_html_result(self):
        """ Gets xml-response from URL
        """
        try:
            if 'proxy_settings' in self.config:
                proxy = urllib2.ProxyHandler(self.config['proxy_settings'])
                opener = urllib2.build_opener(proxy)
                urllib2.install_opener(opener)
            req = urllib2.urlopen(self.url)
            if req.code == 200:
                content = req.read()
                try:
                    decoded_content = content.decode('utf-8')
                except UnicodeDecodeError:
                    decoded_content = content
                self.page = html.document_fromstring(decoded_content)
        except urllib2.URLError:
            self.page = html.etree.Element("html")

    @staticmethod
    def process_row(p):
        """ Process topic's row to text
        :param Element p: Element p for processing
        :rtype: unicode
        """
        for a in p.xpath('.//a'):
            link_text = u'{0}[{1}]'.format(a.text, a.get('href'))
            a.tail = link_text + a.tail if a.tail else link_text
        html.etree.strip_elements(p, 'a', with_tail=False)
        return p.text

    def processed_body_line(self, line):
        """ Beautify content line
        :param basestring line: Content line
        :rtype: list
        """
        lines = []
        line = line.replace('\n', '')
        max_length = int(self.config.get('line_length', 80))
        if len(line) > max_length:
            lines.extend(split_by_length(line, max_length))
        else:
            lines.append(line)
        return lines

    def save(self, path=''):
        """ Save topic to file
            :param basestring path: Path to output file
        """
        path = os.path.join((path or os.getcwd()), self.file_path)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError:
                raise OSError('Could not create a file path. '
                              'Check your options and try again')
        with open(
                os.path.abspath(os.path.join(path, self.file_name)),
                'w+'
        ) as f:
            for line in self.printable_lines:
                f.write(line.encode('utf-8'))

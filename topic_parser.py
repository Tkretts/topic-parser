#!/usr/bin/env python
# coding: utf-8

import yaml
from optparse import OptionParser

from src.parser import Topic


def main():
    """ Main function
    """
    # Init option parser
    parser = OptionParser()
    parser.add_option("-u", "--url", dest="url",
                      help="get topic from URL", metavar="URL")
    parser.add_option("-p", "--path", dest="path",
                      help="save topics to PATH", metavar="PATH")
    parser.add_option("-c", "--config", dest="config_file",
                      help="get config by CONFIG_FILE", metavar="CONFIG_FILE")
    (options, args) = parser.parse_args()

    url = options.url or ''
    config_path = options.config_file or 'config.yaml'
    path = options.path or 'topics'

    # Parse topic
    try:
        config = yaml.load(open(config_path))
    except IOError:
        raise IOError('Could not get config from specified file')

    topic = Topic(url, config)
    topic.save(path)

if __name__ == '__main__':
    main()

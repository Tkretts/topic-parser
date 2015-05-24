Description:
  Parses the news topics from command line by specified url and
  saves it in specified text file without any ads.

Usage:
  Run in command-line:
    ./topic_parser.py [options]
      -u --url - URL for news topic
      -p --path - Path to saving file
      -c --config_file - Configuration file

Config options:
  line_length: Set maximum line's length to format output text

  templates: Set parsing templates for different files.
  Takes 'class' option to find main topic's content and
  'header_class' option to find topic's header (optionally)
  Script gets current template from specified url
  or 'default' template by default.

  proxy_settings: You also can set up a proxy settings if you want some:
    http: 'http://user:pass@proxy:port'
    https: 'https://user:pass@proxy:port'


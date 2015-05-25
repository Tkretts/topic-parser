# coding: utf-8
from distutils.core import setup

setup(
    name='topic_parser',
    version='1.1',
    packages=['', 'src'],
    install_requires=[
        'PyYAML',
        'lxml',
    ],
    url='https://github.com/Tkretts/topic-parser',
    license='',
    author='Topsy Kretts',
    author_email='anton.bogunkov@gmail.com',
    description='Parse news topic from specified URL in command line'
)

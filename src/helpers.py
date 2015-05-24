# coding: utf-8

import re
import urlparse


def url_encode_non_ascii(b):
    """ Encode non-ascii character to url compatible
    :param basestring b: non-ascii character
    :rtype: basestring
    """
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)


def iri_to_uri(iri):
    """ Convert IRI to URI
    :param basestring iri: IRI-string
    :rtype: basestring
    """
    parts = urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti == 1 else url_encode_non_ascii(
            part.encode('utf-8')
        ) for parti, part in enumerate(parts)
    )

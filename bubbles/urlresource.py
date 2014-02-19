# -*- coding: utf-8 -*-

import urllib.request, urllib.error, urllib.parse
import urllib.parse
import codecs
import re

__all__ = (
            "open_resource",
        )


class Resource(object):
    def __init__(self, handle, should_close):
        self.handle = handle
        self.should_close = should_close

    def close(self):
        if self.should_close:
            self.handle.close()


def open_resource(resource, mode=None, encoding=None, binary=False):
    """Get file-like handle for a resource. Conversion:

    * if resource is a string and it is not URL or it is file:// URL, then opens a file
    * if resource is URL then opens urllib2 handle
    * otherwise assume that resource is a file-like handle

    Returns tuple: (handle, should_close) where `handle` is file-like object and `should_close` is
        a flag whether returned handle should be closed or not. Closed should be resources which
        where opened by this method, that is resources referenced by a string or URL.

    """

    if isinstance(resource, str):
        should_close = True
        parts = urllib.parse.urlparse(resource)

        if parts.scheme == '' or parts.scheme == 'file':
            if binary:
                mode = "rb" if not mode else "%sb" % mode
            if mode:
                handle = open(resource, mode=mode,encoding=encoding)
            else:
                handle = open(resource, encoding=encoding)
        else:
            handle = urllib.request.urlopen(resource)
            encoding = encoding or 'utf8'
            reader = codecs.getreader(encoding)
            handle = reader(handle)
    else:
        should_close = False
        handle = resource

    return Resource(handle, should_close)


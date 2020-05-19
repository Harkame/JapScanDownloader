from functools import wraps
import unittest
import os
from distutils.util import strtobool

from nose.plugins.skip import SkipTest

_NET_KEY = "TEST_ENABLE_NETWORK"


def _network_enabled():
    try:
        return strtobool(os.environ[_NET_KEY])
    except KeyError:
        return False


def network_required(f):
    @wraps(f)
    def _wrap(self, *args, **kwargs):
        if not _network_enabled():
            raise SkipTest(f"network required, use {_NET_KEY}=1")

        f(self, *args, **kwargs)

    return _wrap

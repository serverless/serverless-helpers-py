# -*- coding: utf-8 -*-
# MIT Licensed, Copyright (c) 2016 Ryan Scott Brown <sb@ryansb.com>

__all__ = ['load_dotenv', 'get_key', 'set_key', 'unset_key', 'load_envs', 'load_cfn_outputs']

import os
import logging
logger = logging.getLogger()

from dotenv import load_dotenv, get_key, set_key, unset_key
from cfn_detect import load_cfn_outputs

def load_envs(path):
    """Recursively load .env files starting from `path`

    Usage: from your Lambda function, call load_envs with the value __file__ to
    give it the current location as a place to start looking for .env files.

    import serverless_helpers
    serverless_helpers.load_envs(__file__)

    Given the path "foo/bar/myfile.py" and a directory structure like:
        foo
        \---.env
        \---bar
            \---.env
            \---myfile.py

    Values from foo/bar/.env and foo/.env will both be loaded, but values in
    foo/bar/.env will take precedence over values from foo/.env
    """
    path = os.path.abspath(path)
    path, _ = os.path.split(path)


    if path == '/':
        # bail out when you reach top of the FS
        _maybe_load(os.path.join(path, '.env'))
        return
    # load higher envs first
    # closer-to-base environments need higher precedence.
    load_envs(path)
    _maybe_load(os.path.join(path, '.env'))


def _maybe_load(env):
    if os.path.isfile(env):
        logger.debug("Loading .env file %s" % env)
        load_dotenv(env)
    else:
        logger.info(".env file %s does not exist, not loading." % env)

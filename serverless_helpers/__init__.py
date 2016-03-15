# -*- coding: utf-8 -*-
# MIT Licensed, Copyright (c) 2016 Ryan Scott Brown <sb@ryansb.com>

from dotenv import load_dotenv, get_key, set_key, unset_key

def load_envs(path):
    import os
    path, _ = os.path.split(path)
    if path == '/':
        # bail out when you reach top of the FS
        load_dotenv(os.path.join(path, '.env'))
        return
    # load higher envs first
    # closer-to-base environments need higher precedence.
    load_envs(path)
    load_dotenv(os.path.join(path, '.env'))

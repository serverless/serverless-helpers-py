# -*- coding: utf-8 -*-
# MIT Licensed, Copyright (c) 2016 Ryan Scott Brown <sb@ryansb.com>

import os
import mock
import serverless_helpers

def write_testenv(env_fname):
    with open(str(env_fname), 'w') as env:
        env.write('''SERVERLESS_TEST=1
SERVERLESS_STAGE=dev
# this is a comment
SERVERLESS_DATA_MODEL_STAGE=dev
SERVERLESS_PROJECT_NAME=test-sls-helpers''')
    return str(env_fname)

def test_load(tmpdir):
    env_file = write_testenv(tmpdir.join('.env'))
    success = serverless_helpers.load_dotenv(env_file)

    assert success # is True when load succeeds

    assert int(os.getenv('SERVERLESS_TEST')) == 1
    assert os.getenv('SERVERLESS_STAGE') == 'dev'
    assert os.getenv('SERVERLESS_PROJECT_NAME') == 'test-sls-helpers'

def test_load_nonexistent(tmpdir):
    success = serverless_helpers.load_dotenv('/fake/place/.env')
    assert not success

def test_single_key(tmpdir):
    env_file = write_testenv(tmpdir.join('.env'))
    data_stage = serverless_helpers.get_key(env_file, 'SERVERLESS_DATA_MODEL_STAGE')
    assert data_stage == 'dev'
def test_unset_key(tmpdir):
    env_file = write_testenv(tmpdir.join('.env'))
    stage = serverless_helpers.get_key(env_file, 'SERVERLESS_STAGE')
    assert stage == 'dev'
    success, _ = serverless_helpers.unset_key(env_file, 'SERVERLESS_STAGE')
    assert success
    stage = serverless_helpers.get_key(env_file, 'SERVERLESS_STAGE')
    assert stage is None

def test_read_nonexistent(tmpdir):
    env_file = write_testenv(tmpdir.join('.env'))
    data_stage = serverless_helpers.get_key(env_file + 'fooooo', 'SERVERLESS_DATA_MODEL_STAGE')
    assert data_stage is None

def test_write_nonexistent(tmpdir):
    env_file = write_testenv(tmpdir.join('.env'))
    success, key, val = serverless_helpers.set_key(env_file + 'fooooo', 'WRITE', 'nope')
    assert success is None
    assert key == 'WRITE'

def test_get_nonexistent(tmpdir):
    env_file = write_testenv(tmpdir.join('.env'))
    data = serverless_helpers.get_key(env_file, 'NOT_A_THING')
    assert data is None

def test_override_key(tmpdir):
    env_file = write_testenv(tmpdir.join('.env'))
    data_stage = serverless_helpers.get_key(env_file, 'SERVERLESS_DATA_MODEL_STAGE')
    assert data_stage == 'dev'

    serverless_helpers.set_key(env_file, 'SERVERLESS_DATA_MODEL_STAGE', 'overridden')
    data_stage = serverless_helpers.get_key(env_file, 'SERVERLESS_DATA_MODEL_STAGE')

    assert data_stage == 'overridden'

@mock.patch('serverless_helpers.load_dotenv')
def test_get_path_up(load_mock):
    """
    Test that recursive config loading only reads upwards.
    """
    serverless_helpers.load_envs(__file__)
    prev_call = '/'
    for call in load_mock.call_args_list:
        assert call[0][0].startswith(prev_call.replace('.env', ''))
        prev_call = call[0][0]

def test_more_specific_dirs_override(tmpdir):
    """
    Test that .env files closer to the starting dir override
    environments that are higher in the heirarchy
    """
    base = tmpdir.join('.env')
    base.write('OVERRIDE_ME=dev\nCONST=foo')

    serverless_helpers.load_envs(os.path.join(str(tmpdir), 'file.py'))
    assert os.getenv('OVERRIDE_ME') == 'dev'
    assert os.getenv('CONST') == 'foo'

    override = tmpdir.mkdir('first').join('.env')
    override.write('OVERRIDE_ME=prod')

    serverless_helpers.load_envs(os.path.join(str(tmpdir), 'first', 'file.py'))
    assert os.getenv('CONST') == 'foo'
    assert os.getenv('OVERRIDE_ME') == 'prod'

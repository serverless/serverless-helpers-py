# -*- coding: utf-8 -*-
# MIT Licensed, Copyright (c) 2016 Ryan Scott Brown <sb@ryansb.com>

import os
from placebo.utils import placebo_session

import serverless_helpers

def test_unset_environment():
    os.environ.pop('SERVERLESS_PROJECT_NAME', None)
    os.environ.pop('SERVERLESS_STAGE', None)
    stack_name = serverless_helpers.cfn_detect.stack_name()
    assert stack_name == ''

class TestCfnCalls(object):
    @placebo_session
    def test_normal_outputs(self, session):
        os.environ['SERVERLESS_STAGE'] = 'dev'
        os.environ['SERVERLESS_PROJECT_NAME'] = 'mws'
        out = serverless_helpers.load_cfn_outputs(session)
        assert len(out) == 2
        assert 'Description' in out['IamRoleArnLambda']
        assert 'Value' in out['IamRoleArnLambda']
        assert out['IamRoleArnLambda']['Value'].startswith('arn:aws:iam::123456789012')
        assert out['DynamoTable']['Description'] == 'Name of DDB table'

        assert os.getenv('SERVERLESS_CF_IamRoleArnLambda').startswith('arn:aws:iam::123456789012')

    @placebo_session
    def test_notfound(self, session):
        os.environ['SERVERLESS_STAGE'] = 'dev'
        os.environ['SERVERLESS_PROJECT_NAME'] = 'nonexistent'
        out = serverless_helpers.load_cfn_outputs(session)
        assert out == {}

    @placebo_session
    def test_no_outputs(self, session):
        os.environ['SERVERLESS_STAGE'] = 'dev'
        os.environ['SERVERLESS_PROJECT_NAME'] = 'no_outputs'
        out = serverless_helpers.load_cfn_outputs(session)
        assert out == {}

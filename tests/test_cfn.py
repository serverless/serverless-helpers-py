# -*- coding: utf-8 -*-
# MIT Licensed, Copyright (c) 2016 Ryan Scott Brown <sb@ryansb.com>

import serverless_helpers

from placebo.utils import placebo_session

class TestCfnCalls(object):
    @placebo_session
    def test_normal_outputs(self, session):
        import os
        os.environ['SERVERLESS_STAGE'] = 'dev'
        os.environ['SERVERLESS_PROJECT_NAME'] = 'mws'
        out = serverless_helpers.load_cfn_outputs(session)
        assert len(out) == 2
        assert 'Description' in out['IamRoleArnLambda']
        assert 'Value' in out['IamRoleArnLambda']
        assert out['IamRoleArnLambda']['Value'].startswith('arn:aws:iam::123456789012')
        assert out['DynamoTable']['Description'] == 'Name of DDB table'

    @placebo_session
    def test_notfound(self, session):
        import os
        os.environ['SERVERLESS_STAGE'] = 'dev'
        os.environ['SERVERLESS_PROJECT_NAME'] = 'nonexistent'
        out = serverless_helpers.load_cfn_outputs(session)
        assert out == {}

    @placebo_session
    def test_no_outputs(self, session):
        import os
        os.environ['SERVERLESS_STAGE'] = 'dev'
        os.environ['SERVERLESS_PROJECT_NAME'] = 'no_outputs'
        out = serverless_helpers.load_cfn_outputs(session)
        assert out == {}

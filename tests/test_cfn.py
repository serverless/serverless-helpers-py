# -*- coding: utf-8 -*-
# MIT Licensed, Copyright (c) 2016 Ryan Scott Brown <sb@ryansb.com>

import mock
import serverless_helpers

def test_cfn_stack_no_outputs():
    fake_client = mock.Mock()
    fake_describe = mock.MagicMock(return_value={'Stacks': []})
    fake_client.describe_stacks = fake_describe
    out = serverless_helpers.load_cfn_outputs(cfn_client=fake_client)
    assert len(out) == 0

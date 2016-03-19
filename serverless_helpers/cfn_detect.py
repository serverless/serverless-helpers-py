# -*- coding: utf-8 -*-
# MIT Licensed, Copyright (c) 2016 Ryan Scott Brown <sb@ryansb.com>

import os
import boto3


PREFIX = u'SERVERLESS_CF_'


def stack_name():
    return u'%s-%s-r' % (
        os.getenv('SERVERLESS_PROJECT_NAME'),
        os.getenv('SERVERLESS_STAGE')
    )


def load_cfn_outputs(cfn_client=None):
    """
    Load all stack outputs into the environment, with prefix "SERVERLESS_CF_".
    Also returns a dict of return values.

    {
      "OutputName": {
        "Value": <thevalue>,
        "Description": "what this value means"
      }
    }
    """
    if cfn_client is None:
        cfn_client = boto3.client('cloudformation')
    stacks = cfn_client.describe_stacks(StackName=stack_name())
    if not len(stacks['Stacks']):
        # no stacks, nuts
        return {}

    outputs = stacks['Stacks'][0]['Outputs']
    reformatted = {
        o['OutputKey']: {
            'Value': o['OutputValue'],
            'Description': o['Description']
        } for o in outputs
    }
    for key, value in reformatted.items():
        os.environ.setdefault(PREFIX + key, value['Value'])

    return reformatted

# -*- coding: utf-8 -*-
# MIT Licensed, Copyright (c) 2016 Ryan Scott Brown <sb@ryansb.com>

import os
import logging
import boto3
import botocore.exceptions as core_exc

logger = logging.getLogger()
PREFIX = u'SERVERLESS_CF_'


def stack_name():
    if not (os.getenv('SERVERLESS_PROJECT_NAME') or
            os.getenv('SERVERLESS_STAGE')):
        logger.warning(
            'Could not get SERVERLESS_PROJECT_NAME or SERVERLESS_STAGE from '
            'environment. This probably means the .env file was not loaded. '
            'Make sure you call `serverless_helpers.load_envs(__file__)` '
            'first.')

    return u'%s-%s-r' % (
        os.getenv('SERVERLESS_PROJECT_NAME'),
        os.getenv('SERVERLESS_STAGE')
    )


def load_cfn_outputs(boto3_session=None):
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
    if boto3_session is None:
        cfn_client = boto3.client('cloudformation')
    else:
        cfn_client = boto3_session.client('cloudformation')
    try:
        stacks = cfn_client.describe_stacks(StackName=stack_name())
    except core_exc.ClientError as e:
        import json
        logger.exception('Failed when retrieving stack')
        logger.error('Full response from AWS: %s' % json.dumps(e.response))
        return {}
    else:
        logger.debug('Retrieved stack %s from CFN API' % stack_name())

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

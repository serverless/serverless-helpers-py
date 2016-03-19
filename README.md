## serverless_helpers

This library isn't *required* for writing Python in the [serverless][sls], but
it does make your life easier by handling things like environment variables for
you.

## Usage

```
import serverless_helpers

# all .env files are loaded into the environment
serverless_helpers.load_envs(__file__)

# Loads stack outputs into environment variables as `SERVERLESS_CF_[output name]`
serverless_helpers.load_cfn_outputs()

import os
os.getenv('SERVERLESS_STAGE') # dev

# get role ARN from default serverless CloudFormation stack
os.getenv('SERVERLESS_CF_IamRoleArnLambda') # arn:aws:iam::123456789012:....

# alternate way to read roles
outputs = serverless_helpers.load_cfn_outputs()
outputs['IamRoleArnLambda'] # arn:aws:iam::123456789012:....
```

## License

This code is released under the MIT software license, see LICENSE file for
details. No warranty of any kind is included, and the copyright notice must be
included in redistributions.

*Notable exception*: `dotenv.py` is from
[python-dotenv](https://github.com/theskumar/python-dotenv) to remove
dependencies on click and ordereddict for performance/deployment size reasons.
Read the license contained in `dotenv.py` for details on its creators and
license conditions.

[sls]: http://serverless.com/

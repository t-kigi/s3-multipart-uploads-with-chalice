#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import yaml

import aws_cdk as cdk
from pycdk import InitStack


conffile = os.environ.get('CONFIG_FILE') or 'config.yaml'
with open(conffile) as fh:
    conf = yaml.safe_load(fh)['AWSResources']


app = cdk.App()
init_stack = InitStack(app, 'S3ForUploadInitStack', conf)

app.synth()

#!/usr/bin/python
# -*- coding: utf-8 -*-

import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    aws_s3 as cdk_s3,
)


class InitStack(cdk.Stack):
    """ Setup Sangria AWS Resources required before Chalice deployment """

    # S3 Bucket for static resources
    bucket: cdk_s3.Bucket

    def __init__(self, scope: Construct, construct_id: str,
                 conf: dict, **kwargs) -> None:
        kwargs['stack_name'] = f'{construct_id}{conf["StageName"]}'

        super().__init__(scope, construct_id, **kwargs)

        # Define S3 Bucket and settings to allow access from CloudFront
        prefix = conf.get('StageName', 'local')
        allowed_origins = conf['S3'].get('AllowOrigins', [])
        bucket_cors = cdk_s3.CorsRule(
            allowed_headers=['*'],
            allowed_methods=[
                cdk_s3.HttpMethods.PUT
            ],
            allowed_origins=allowed_origins,
            exposed_headers=['ETag']
        )
        bucket_name = '.'.join([
            prefix, conf['S3'].get('BucketName')
        ])

        lifecycle_rules = [
            # マルチパートアップロード失敗を時間経過で自動消去
            cdk_s3.LifecycleRule(
                abort_incomplete_multipart_upload_after=cdk.Duration.days(3),
                prefix='uploads/'
            ),
        ]
        self.bucket = cdk_s3.Bucket(
            self, 'UploadsBucket',
            bucket_name=bucket_name,
            encryption=cdk_s3.BucketEncryption.S3_MANAGED,
            block_public_access=cdk_s3.BlockPublicAccess.BLOCK_ALL,
            cors=[bucket_cors],
            lifecycle_rules=lifecycle_rules
        )
        cdk.CfnOutput(self, 'UploadBucketName',
                      value=self.bucket.bucket_name)

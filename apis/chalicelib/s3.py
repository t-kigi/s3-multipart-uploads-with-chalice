#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
S3 の操作を行うためのヘルパモジュールです。
"""

import mimetypes
import logging

import boto3


logger = logging.getLogger(__name__)


class S3MultiPartUploader:
    """ マルチパートアップロード用のロジックです """

    def __init__(
        self, session: boto3.session.Session,
        bucketname: str, upload_prefix: str = 'uploads/tmp/'
    ):
        self.session = session
        self.client = session.client('s3')
        self.bucketname = bucketname
        self.upload_prefix = upload_prefix

    def _content_type(self, suffix: str) -> str:
        """ リクエストする ContentType を拡張子から判定します """
        if not bool(suffix):
            # 未指定の場合は binary
            return 'application/octet-stream'
        suffix = suffix if suffix.startswith('.') else f'.{suffix}'
        content_type = mimetypes.guess_type(f'a{suffix}')[0]
        return content_type or 'application/octet-stream'

    def _create_multipart_upload_url(
        self, key: str, upload_id: str, part: int,
        expires_seconds: int = 3600
    ):
        """ マルチパートアップロード用の URL を生成します """
        return self.client.generate_presigned_url(
            ClientMethod='upload_part',
            Params={
                'Bucket': self.bucketname,
                'Key': key,
                'UploadId': upload_id,
                'PartNumber': part,
            })

    def start_multipart_upload(
        self, filename: str, total_part: int,
        suffix: str = None, expires_seconds: int = 7200,
        temporary_prefix: str = None
    ):
        """ マルチパートアップロードを開始します """
        prefix = temporary_prefix or self.upload_prefix
        key = f'{prefix}{filename}'
        content_type = self._content_type(suffix)
        res = self.client.create_multipart_upload(
            Bucket=self.bucketname, Key=key
        )
        parts = [
            {
                'part': idx+1,
                'url': self._create_multipart_upload_url(
                    res['Key'], res['UploadId'], idx+1
                ),
            } for idx in range(total_part)
        ]

        return {
            'UploadId': res['UploadId'],
            'UploadKey': key,
            'ContentType': content_type,
            'Parts': parts,
        }

    def complete_multipart_upload(self, key: str, upload_id: str,
                                  parts: list):
        """ マルチパートアップロードを完了させます """
        try:
            self.client.complete_multipart_upload(
                Bucket=self.bucketname,
                Key=key,
                MultipartUpload={'Parts': parts},
                UploadId=upload_id)
            return True
        except Exception as err:
            logging.exception(err)
            return False

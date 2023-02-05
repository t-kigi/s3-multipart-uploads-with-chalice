#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import uuid
import mimetypes

import boto3
from chalice import Chalice, Response, NotFoundError

from chalicelib.s3 import S3MultiPartUploader
from chalicelib.render import Engine, StaticTemplatePicker

from typing import Optional


app = Chalice(app_name='apis')

# S3 操作用
profile = os.environ.get('PROFILE')
if profile:
    session = boto3.session.Session(profile_name=profile)
else:
    session = boto3.session.Session()
s3 = S3MultiPartUploader(session, os.environ['BUCKET_NAME'])

# テンプレートエンジン
project_dir = os.path.dirname(__file__)
template_root = os.path.join(project_dir, 'chalicelib', 'templates')
engine = Engine(StaticTemplatePicker(template_root))


@app.route('/')
def index():
    return engine.render('index.html')


def _static_content_type(filepath):
    ''' static file 用の Content-Type を返す '''
    content_type = mimetypes.guess_type(filepath.lower())[0]
    return content_type or 'application/json'


@app.route('/static/js/{filename}')
def js_static(filename: str):
    """ static file の読み込み """
    filepath = os.path.join(
        project_dir, 'chalicelib', 'static', 'js', filename
    )
    print(filepath)

    try:
        # テキストでの読み込み
        with open(filepath, 'r') as fp:
            return Response(body=fp.read(), status_code=200, headers={
                'Content-Type': _static_content_type(filepath),
            })
    except Exception:
        raise NotFoundError(filename)


def _json(body: dict, status: int = 200) -> Response:
    """ application/json を返すレスポンスです """
    headers = {
        'Content-Type': 'application/json',
    }
    return Response(body=body, status_code=status, headers=headers)


@app.route('/api/multipart_upload/start/{ext}',
           methods=['PUT'])
def start_multipart_upload(ext: Optional[str] = None):
    """ 動画のマルチアップロードの開始処理 """
    params = app.current_request.json_body or {}
    total_part = params.get('TotalPart', 0)
    if total_part < 0:
        return _json({
            'message': 'TotalPart: int required',
        }, status=400)
    if ext:
        filename = '.'.join([str(uuid.uuid4()), ext])
    else:
        filename = str(uuid.uuid4())

    res = s3.start_multipart_upload(filename, total_part, suffix=ext)
    return _json(res)


@app.route('/api/multipart_upload/complete',
           methods=['PUT'])
def complete_multipart_upload():
    """ マルチアップロードの完了通知 """
    params = app.current_request.json_body or {}
    res = s3.complete_multipart_upload(
        params['Key'], params['UploadId'], params['Parts'])
    return _json({
        'Success': res,
    })

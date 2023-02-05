#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
テンプレートエンジンのレンダリング機能を実装します
"""

from jinja2 import Environment, FileSystemLoader, select_autoescape
from chalice import Response


class StaticTemplatePicker:
    """ テンプレートを固定ファイルから取得して提供するクラスです """
    def __init__(self, rootpath):
        self.rootpath = rootpath
        self.env = Environment(
            loader=FileSystemLoader([rootpath]),
            autoescape=select_autoescape(['html', 'xml']))

    def get(self, template_path):
        """ テンプレートを取得します """
        return self.env.get_template(template_path)


class Engine:
    """ レンダリングを行います """
    def __init__(self, picker: StaticTemplatePicker):
        self.picker = picker

    def render(self, tplname: str, params: dict = None) -> str:
        """ レンダリングを実施して単なるテキストを返します """
        params = params or {}
        tpl = self.picker.get(tplname)
        headers = {
            'Content-Type': 'text/html'
        }
        return Response(
            status_code=200, headers=headers,
            body=tpl.render(**params))

# -*- coding: utf-8 -*-


import yaml
import os


class ParseYaml(object):
    def __init__(self):
        self.yaml_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'config.yml')

    def __call__(self):
        config = yaml.load(file(self.yaml_file))
        return config


conf = ParseYaml()()
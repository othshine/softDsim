import os
from dataclasses import dataclass
from django.conf import settings

from yaml import load, FullLoader


class Team:
    pass


class Member:
    pass


@dataclass
class SkillType:
    def __init__(self, stype: str, config_path=os.path.join(settings.BASE_DIR, 'parameter.yaml')):
        self.stype = stype
        self.config_path = config_path
        self.setattr()

    def setattr(self):
        print(self.config_path)
        with open(self.config_path) as y:
            data = load(y, Loader=FullLoader)
            data = data['skill-levels'][self.stype]
        self.salary = data['salary']
        self.error_rate = data['error-rate']
        self.throughput = data['throughput']

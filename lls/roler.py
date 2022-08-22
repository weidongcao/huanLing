# -*- coding:utf-8 -*-
from entity.entity import Entity


class Roler(Entity):
    table_name = "roler"

    def __init__(self,
                 rid=None,
                 role=None,
                 task=None,
                 create_time=None,
                 update_time=None,
                 **kwargs):
        self.rid = rid
        self.role = role
        self.task = task
        self.create_time = create_time
        self.update_time = update_time

        super().__init__(**kwargs)


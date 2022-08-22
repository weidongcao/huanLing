# -*- coding:utf-8 -*-
from entity.entity import Entity


class Egypt(Entity):
    table_name = "egypt"

    def __init__(self,
                 eid=None,
                 nickname=None,
                 type=None,
                 role=None,
                 supervisor=None,
                 union=None,
                 part=None,
                 area=None,
                 fight_time=None,
                 status=None,
                 create_time=None,
                 update_time=None,
                 **kwargs):
        self.eid = eid
        self.nickname = nickname
        self.type = type
        self.role = role
        self.supervisor = supervisor
        self.union = union
        self.part = part
        self.area = area
        self.fight_time = fight_time
        self.status = status
        self.create_time = create_time
        self.update_time = update_time

        super().__init__(**kwargs)


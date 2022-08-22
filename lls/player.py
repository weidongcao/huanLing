# -*- coding:utf-8 -*-
from entity.entity import Entity


class player(Entity):
    table_name = "player"

    def __init__(self,
                 lid=None,
                 chat_name=None,
                 nickname=None,
                 strength=None,
                 type="",
                 vip=0,
                 officer=None,
                 infantry=0,
                 cavalry=0,
                 archers=0,
                 inf_outfit=0,
                 inf_outfit_pro=0,
                 cav_outfit=0,
                 cav_outfit_pro=0,
                 arc_outfit=0,
                 arc_outfit_pro=0,
                 **kwargs):
        self.lid = lid
        self.chat_name = chat_name
        self.nickname = nickname
        self.strength = strength
        self.type = type
        self.vip = vip
        self.officer = officer
        self.infantry = infantry
        self.cavalry = cavalry
        self.archers = archers
        self.inf_outfit = inf_outfit
        self.inf_outfit_pro = inf_outfit_pro
        self.cav_outfit = cav_outfit
        self.cav_outfit_pro = cav_outfit_pro
        self.arc_outfit = arc_outfit
        self.arc_outfit_pro = arc_outfit_pro

        super().__init__(**kwargs)

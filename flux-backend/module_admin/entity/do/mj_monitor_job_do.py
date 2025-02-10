# -*- coding:utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, SmallInteger, JSON
from config.database import BaseMixin, Base


class MjMonitorJob(Base, BaseMixin):
    __tablename__ = "mj_monitor_job"

    batch_size = Column(Integer, comment='批处理大小')

    create_source = Column(String(50), comment='创建来源')

    current_status = Column(String(50), comment='当前状态')

    discord_url = Column(String(255), comment='Discord URL')

    enqueue_time = Column(DateTime, comment='提交时间')

    event_type = Column(String(50), comment='事件类型')

    full_command = Column(Text, comment='咒语')

    height = Column(Integer, comment='图像高度')

    job_id = Column(String(36), comment='job_id')

    job_type = Column(String(50), comment='job类型')

    liked_by_user = Column(SmallInteger, comment='是否喜欢')

    liked_by_user_in_room = Column(JSON, comment='喜欢状态')

    mj_id = Column(Integer, comment='mj_id')

    parent_grid = Column(Integer, comment='相关的父网格')

    parent_id = Column(String(36), comment='父事件job_id')

    published = Column(SmallInteger, comment='是否发布')

    rating = Column(Integer, comment='评分')

    shown = Column(SmallInteger, comment='是否显示')

    username = Column(String(50), comment='用户名')

    user_hidden = Column(SmallInteger, comment='是否隐藏')

    user_id = Column(String(36), comment='mj_user_id')

    width = Column(Integer, comment='图像宽度')


# -*- coding:utf-8 -*-

from sqlalchemy import Column, ForeignKey, String, DateTime, Integer
from config.database import BaseMixin, Base


class MjAccount(Base, BaseMixin):
    __tablename__ = "mj_account"

    cookie = Column(String(6000), nullable=False, comment='Cookie')

    email = Column(String(200), comment='邮箱')

    error_msg = Column(String(1000), comment='异常信息')

    expire_time = Column(DateTime, comment='到期时间')

    last_monitor_time = Column(DateTime, comment='监控时间')

    mj_id = Column(Integer, nullable=False, comment='mj_id')

    monitor_status = Column(String(50), comment='监控状态')

    plan = Column(String(255), comment='订阅计划')

    remark = Column(String(1000), comment='备注')

    status = Column(String(255), comment='订阅状态')

    subscribe_time = Column(DateTime, comment='开通时间')

    token = Column(String(255), comment='Token')

    total_jobs = Column(Integer, comment='总出图数')

    user_id = Column(String(36), comment='user_id')


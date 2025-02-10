# -*- coding:utf-8 -*-
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import List, Literal, Optional, Union
from module_admin.annotation.pydantic_annotation import as_query


class MjAccountModel(BaseModel):
    """
    表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)
    cookie: Optional[str] =  Field(default=None, description='Cookie')
    create_time: Optional[datetime] =  Field(default=None, description='创建时间')
    del_flag: Optional[str] =  Field(default=None, description='删除标志(0代表存在 2代表删除)')
    email: Optional[str] =  Field(default=None, description='邮箱')
    error_msg: Optional[str] =  Field(default=None, description='异常信息')
    expire_time: Optional[datetime] =  Field(default=None, description='到期时间')
    id: Optional[int] =  Field(default=None, description='自增主键')
    last_monitor_time: Optional[datetime] =  Field(default=None, description='监控时间')
    mj_id: Optional[int] =  Field(default=None, description='mj_id')
    monitor_status: Optional[str] =  Field(default=None, description='监控状态')
    plan: Optional[str] =  Field(default=None, description='订阅计划')
    remark: Optional[str] =  Field(default=None, description='备注')
    status: Optional[str] =  Field(default=None, description='订阅状态')
    subscribe_time: Optional[datetime] =  Field(default=None, description='开通时间')
    begin_subscribe_time: Optional[datetime] =  Field(default=None, description='开通时间最小值')
    end_subscribe_time: Optional[datetime] =  Field(default=None, description='开通时间最大值')
    token: Optional[str] =  Field(default=None, description='Token')
    total_jobs: Optional[int] =  Field(default=None, description='总出图数')
    update_time: Optional[datetime] =  Field(default=None, description='更新时间')
    user_id: Optional[str] =  Field(default=None, description='user_id')


@as_query
class MjAccountPageModel(MjAccountModel):
    """
    分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
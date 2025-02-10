# -*- coding:utf-8 -*-
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import List, Literal, Optional, Union
from module_admin.annotation.pydantic_annotation import as_query


class MjMonitorJobModel(BaseModel):
    """
    表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)
    batch_size: Optional[int] =  Field(default=None, description='批处理大小')
    create_source: Optional[str] =  Field(default=None, description='创建来源')
    create_time: Optional[datetime] =  Field(default=None, description='创建时间')
    begin_create_time: Optional[datetime] =  Field(default=None, description='创建时间最小值')
    end_create_time: Optional[datetime] =  Field(default=None, description='创建时间最大值')
    current_status: Optional[str] =  Field(default=None, description='当前状态')
    del_flag: Optional[str] =  Field(default=None, description='删除标志')
    discord_url: Optional[str] =  Field(default=None, description='Discord URL')
    enqueue_time: Optional[datetime] =  Field(default=None, description='提交时间')
    begin_enqueue_time: Optional[datetime] =  Field(default=None, description='提交时间最小值')
    end_enqueue_time: Optional[datetime] =  Field(default=None, description='提交时间最大值')
    event_type: Optional[str] =  Field(default=None, description='事件类型')
    full_command: Optional[str] =  Field(default=None, description='咒语')
    height: Optional[int] =  Field(default=None, description='图像高度')
    id: Optional[int] =  Field(default=None, description='自增主键')
    job_id: Optional[str] =  Field(default=None, description='job_id')
    job_type: Optional[str] =  Field(default=None, description='job类型')
    liked_by_user: Optional[int] =  Field(default=None, description='是否喜欢')
    # liked_by_user_in_room: Optional[dict] =  Field(default=None, description='喜欢状态')
    mj_id: Optional[int] =  Field(default=None, description='mj_id')
    parent_grid: Optional[int] =  Field(default=None, description='相关的父网格')
    parent_id: Optional[str] =  Field(default=None, description='父事件job_id')
    published: Optional[int] =  Field(default=None, description='是否发布')
    rating: Optional[int] =  Field(default=None, description='评分')
    shown: Optional[int] =  Field(default=None, description='是否显示')
    update_time: Optional[datetime] =  Field(default=None, description='更新时间')
    begin_update_time: Optional[datetime] =  Field(default=None, description='更新时间最小值')
    end_update_time: Optional[datetime] =  Field(default=None, description='更新时间最大值')
    username: Optional[str] =  Field(default=None, description='用户名')
    user_hidden: Optional[int] =  Field(default=None, description='是否隐藏')
    user_id: Optional[str] =  Field(default=None, description='mj_user_id')
    width: Optional[int] =  Field(default=None, description='图像宽度')


@as_query
class MjMonitorJobPageModel(MjMonitorJobModel):
    """
    分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
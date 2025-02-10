# -*- coding:utf-8 -*-

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.common_util import CamelCaseUtil, export_list2excel
from utils.page_util import PageResponseModel
from module_admin.dao.mj_monitor_job_dao import MjMonitorJobDao
from module_admin.entity.do.mj_monitor_job_do import MjMonitorJob
from module_admin.entity.vo.mj_monitor_job_vo import MjMonitorJobPageModel, MjMonitorJobModel


class MjMonitorJobService:
    """
    用户管理模块服务层
    """

    @classmethod
    async def get_mj_monitor_job_list(cls, query_db: AsyncSession, query_object: MjMonitorJobPageModel, data_scope_sql: str) -> [list | PageResponseModel]:
        mj_monitor_job_list = await MjMonitorJobDao.get_mj_monitor_job_list(query_db, query_object, data_scope_sql, is_page=True)
        return mj_monitor_job_list

    @classmethod
    async def get_mj_monitor_job_by_id(cls, query_db: AsyncSession, mj_monitor_job_id: int) -> MjMonitorJobModel:
        mj_monitor_job = await  MjMonitorJobDao.get_by_id(query_db, mj_monitor_job_id)
        mj_monitor_job_model = MjMonitorJobModel(**CamelCaseUtil.transform_result(mj_monitor_job))
        return mj_monitor_job_model


    @classmethod
    async def add_mj_monitor_job(cls, query_db: AsyncSession, query_object: MjMonitorJobModel) -> MjMonitorJobModel:
        mj_monitor_job = await MjMonitorJobDao.add_mj_monitor_job(query_db, query_object)
        mj_monitor_job_model = MjMonitorJobModel(**CamelCaseUtil.transform_result(mj_monitor_job))
        return mj_monitor_job_model


    @classmethod
    async def update_mj_monitor_job(cls, query_db: AsyncSession, query_object: MjMonitorJobModel) -> MjMonitorJobModel:
        mj_monitor_job = await MjMonitorJobDao.edit_mj_monitor_job(query_db, query_object)
        mj_monitor_job_model = MjMonitorJobModel(**CamelCaseUtil.transform_result(mj_monitor_job))
        return mj_monitor_job_model


    @classmethod
    async def del_mj_monitor_job(cls, query_db: AsyncSession, mj_monitor_job_ids: List[str]):
        await MjMonitorJobDao.del_mj_monitor_job(query_db, mj_monitor_job_ids)


    @classmethod
    async def export_mj_monitor_job_list(cls, query_db: AsyncSession, query_object: MjMonitorJobPageModel, data_scope_sql) -> bytes:
        mj_monitor_job_list = await MjMonitorJobDao.get_mj_monitor_job_list(query_db, query_object, data_scope_sql, is_page=False)
        mapping_dict = {
            'createSource': '创建来源 ',
            'currentStatus': '当前状态 ',
            'discordUrl': 'Discord URL ',
            'enqueueTime': '提交时间 ',
            'eventType': '事件类型 ',
            'fullCommand': '咒语 ',
            'id': '自增主键 ',
            'jobId': 'job_id ',
            'jobType': 'job类型 ',
            'mjId': 'mj_id ',
            'parentId': '父事件job_id ',
            'updateTime': '更新时间 ',
            'username': '用户名 ',
            'userId': 'mj_user_id ',
        }
        new_data = [
            {mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in mj_monitor_job_list
        ]
        binary_data = export_list2excel(new_data)
        return binary_data